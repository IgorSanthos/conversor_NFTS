import os
import tempfile
from flask import Flask, request, render_template, send_file, jsonify, url_for
import pandas as pd
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Definir um diretório temporário para salvar os arquivos
temp_dir = tempfile.gettempdir()

# Helper function
def allowed_file(filename):
    return '.' in filename

def replacement_date(x, y):
    x_part = x[:10]
    y_part = y[:10]
    x = y_part + x[10:]
    y = x_part + y[10:]
    return x, y

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'Nenhum arquivo selecionado'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'Nenhum arquivo selecionado'}), 400

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(temp_dir, filename)  # Salvar no diretório temporário
        file.save(file_path)
        
        # Processar o arquivo
        try:
            df = pd.read_csv(file_path, encoding='latin1', sep=';')
            df = df.astype(str)
            df = df.replace('nan', '')
            df['Número do Documento'] = df['Número do Documento'].astype(str).str.replace('.0', '')
            df['Data Hora Emissão NFTS'], df['Data da Prestação de Serviços'] = zip(*df.apply(lambda row: replacement_date(row['Data Hora Emissão NFTS'], row['Data da Prestação de Serviços']), axis=1))
            
            new_numeracoes = []
            count_dict = {}
            for num in df['Número do Documento']:
                if num in count_dict:
                    count_dict[num] += 1
                else:
                    count_dict[num] = 1
                if count_dict[num] > 1:
                    new_value = f"{num}-{count_dict[num] - 1}"
                else:
                    new_value = str(num)
                new_numeracoes.append(new_value)
            df['Número do Documento'] = new_numeracoes
            df.loc[:, 'Nº NFTS'] = df.loc[:, 'Número do Documento']

            processed_file_path = os.path.join(temp_dir, f"alterado_{filename}")  # Salvar o arquivo processado no diretório temporário
            df.to_csv(processed_file_path, index=False, sep=';', encoding='latin1')
            
            download_url = url_for('download_file', filename=f"alterado_{filename}")  # Usar o mesmo nome para o arquivo processado
            return jsonify({'status': 'success', 'message': 'Arquivo processado com sucesso!', 'download_url': download_url})
        
        except Exception as e:
            # Log da exceção para fins de depuração
            print(f"Erro ao processar o arquivo: {e}")
            return jsonify({'status': 'error', 'message': f"Erro ao processar o arquivo: {str(e)}"}), 500
    else:
        return jsonify({'status': 'error', 'message': 'Tipo de arquivo não permitido'}), 400

@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_file(os.path.join(temp_dir, filename), as_attachment=True)
    except Exception as e:
        # Log da exceção para fins de depuração
        print(f"Erro ao baixar o arquivo: {e}")
        return jsonify({'status': 'error', 'message': f"Erro ao baixar o arquivo: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
