# --- Étape 1 : Récupération du binaire officiel 'uv' ---
FROM ghcr.io/astral-sh/uv:latest AS uv-bin

# --- Étape 2 : Image finale Python légère ---
FROM python:3.11-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# Copie du binaire 'uv' depuis la première étape dans le PATH du conteneur
COPY --from=uv-bin /uv /uvx /bin/

# Évite que Python écrive des fichiers .pyc et bufferise les logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Optimisations recommandées pour uv dans Docker
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Configuration non-sensible pour le Model Runner
ENV GEMMA_MODEL=ai/gemma4:latest

# Définit le dossier de travail dans le conteneur
WORKDIR /app

# Crée un utilisateur non-privilégié pour la sécurité
RUN useradd -m appuser && chown -R appuser /app

# Copie d'abord le fichier des dépendances
COPY requirements.txt .

# Installe les dépendances à une vitesse fulgurante grâce à uv (en mode --system)
RUN uv pip install --no-cache-dir --system -r requirements.txt

# Copie le reste du code source de l'application en l'attribuant à l'utilisateur
COPY --chown=appuser:appuser src/ ./src

# Bascule vers l'utilisateur non-privilégié
USER appuser

# Commande par défaut pour lancer l'application
CMD ["python", "src/main.py"]