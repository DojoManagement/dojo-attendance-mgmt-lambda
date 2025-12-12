#!/bin/bash

set -e  # Encerra o script se algum comando falhar

# Diretórios e arquivos
SOURCE_DIR="app"                        # Altere se o código estiver em outro lugar
BUILD_DIR="lambda_build"
ZIP_FILE="lambda_package.zip"
REQUIREMENTS_FILE="$SOURCE_DIR/requirements.txt"

echo "🔧 Limpando build anterior..."
sudo rm -rf "$BUILD_DIR" "$ZIP_FILE"

echo "📁 Criando diretório de build: $BUILD_DIR"
sudo mkdir -p "$BUILD_DIR"

echo "📦 Instalando dependências do requirements.txt..."
sudo pip install -r "$REQUIREMENTS_FILE" -t "$BUILD_DIR"

echo "📄 Copiando arquivos da aplicação para o diretório de build..."
sudo cp -r "$SOURCE_DIR"/* "$BUILD_DIR/"

sudo cp -r ../dojo-commons/dojocommons "$BUILD_DIR/"

echo "📁 listando arquivos do $BUILD_DIR"
ls -l "$BUILD_DIR"


# Copie outros diretórios necessários (modifique conforme seu projeto)
#if [ -d "$SOURCE_DIR/athletemgmt" ]; then
#  cp -r "$SOURCE_DIR/dojocommons" "$BUILD_DIR/"
#fi

echo "🗜️ Criando o pacote .zip: $ZIP_FILE"
cd "$BUILD_DIR"
sudo zip -r9 "../$ZIP_FILE" . > /dev/null
cd ..
sudo chmod 777 "$ZIP_FILE"

sudo rm -rf "$BUILD_DIR"

ls -l "$ZIP_FILE"

echo "✅ Build completo: $ZIP_FILE está pronto para uso no Terraform"
