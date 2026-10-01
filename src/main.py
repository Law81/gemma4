"""Application entry point."""
from datetime import date

import torch
from transformers import AutoModelForMultimodalLM, AutoProcessor, BitsAndBytesConfig

MODEL_ID = "google/gemma-4-31B-it"


def main():
    if not torch.cuda.is_available():
        raise RuntimeError(
            "CUDA est indisponible. Installez une version de PyTorch compatible "
            "CUDA et vérifiez que le GPU est accessible au processus."
        )

    device = torch.device("cuda:0")
    dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
    print(f"GPU CUDA utilisé : {torch.cuda.get_device_name(device)}")

    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=dtype,
        bnb_4bit_use_double_quant=True,
    )

    processor = AutoProcessor.from_pretrained(MODEL_ID)
    model = AutoModelForMultimodalLM.from_pretrained(
        MODEL_ID,
        dtype=dtype,
        quantization_config=quantization_config,
        device_map={"": device.index},
    )

    today = date.today().isoformat()
    messages = [
        {
            "role": "system",
            "content": (
                "Tu es un assistant spécialisé dans la recherche d'offres d'emploi "
                "pour les métiers de Data Analyst et Data Scientist. Réponds toujours "
                "en français. N'invente jamais d'offres, de dates, de salaires ou de "
                "liens : si tu ne peux pas vérifier une information ou accéder aux "
                "annonces en ligne, indique-le clairement."
            ),
        },
        {
            "role": "user",
            "content": (
                "Recherche sur plusieurs sites d'emploi et pages carrières "
                "d'entreprises des offres de Data Analyst et Data Scientist "
                "(y compris les intitulés équivalents en français ou en anglais).\n"
                f"La date du jour est le {today}. "
                "Ne retiens que les offres publiées au cours des 30 derniers jours "
                "et dont la date de publication est vérifiable.\n"
                "Les postes doivent être situés en France, y compris le télétravail "
                "ou le mode hybride depuis la France. Exclue les postes situés à "
                "l'étranger, même s'ils sont annoncés comme télétravail.\n"
                "Ne retiens que les contrats CDI ou CDD, avec un salaire brut annuel "
                "compris entre 30 000 et 50 000 euros et une expérience demandée "
                "inférieure à 5 ans. Exclue les offres dont le salaire ou la date "
                "de publication ne peut pas être vérifié.\n"
                "Présente les résultats pour être enregistrés dans "
                f"annonces_{today}.csv. "
                "Retourne uniquement le contenu CSV, sans bloc Markdown, avec le "
                "point-virgule comme séparateur et une ligne d'en-tête. "
                "Utilise exactement ces colonnes : Lien de l'offre;Nom de "
                "l'entreprise;Lieu;Date de publication;Type de contrat. "
                "Mets les dates au format AAAA-MM-JJ et fournis le lien direct "
                "vers chaque annonce. Si aucune offre ne peut être vérifiée, "
                "ne fabrique aucun résultat."
            ),
        },
    ]

    inputs = processor.apply_chat_template(
        messages,
        tokenize=True,
        return_dict=True,
        return_tensors="pt",
        add_generation_prompt=True,
        enable_thinking=True,
    ).to(device)
    input_len = inputs["input_ids"].shape[-1]

    outputs = model.generate(**inputs, max_new_tokens=256*10)
    response = processor.decode(outputs[0][input_len:], skip_special_tokens=False)

    print(processor.parse_response(response, prefix="<|think|>"))


if __name__ == "__main__":
    main()