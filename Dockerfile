FROM ruby:3.2-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    python3.12 \
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
RUN pip install --no-cache-dir -r requirements.txt

# Ejecutar scripts Python
RUN python3 caducidad.py && python3 calfile.py

# Exponer puerto
EXPOSE 4000

# Comando por defecto
CMD ["bundle", "exec", "jekyll", "serve", "--host", "0.0.0.0", "--port", "4000", "--livereload"]
