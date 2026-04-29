FROM ruby:3.2-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /site

# Copiar Gemfile y Gemfile.lock
COPY Gemfile* ./

# Instalar gemas
RUN bundle install

# Copiar el resto del proyecto
COPY . .

# Instalar dependencias Python
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

# Exponer puerto
EXPOSE 4000

# Comando por defecto
CMD ["sh", "-c", "python3 caducidad.py && python3 calfile.py && bundle exec jekyll serve --host 0.0.0.0 --port 4000 --livereload"]
