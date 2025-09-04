# app.py
from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize Groq client
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

@app.route('/', methods=['GET'])
def index():
    # Edad
    age = [
    '1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33',
    '34','35','36','37','38','39','40','41','42','43','44','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59','60','61','62','63','64',
    '65','66','67','68','69','70','71','72','73','74','75','76','77','78','79','80','81','82','83','84','85','86','87','88','89','90','91','92','93','94','95',
    '96','97','98','99'
    ]
    return render_template('index.html', age=age)

@app.route('/recommend', methods=['POST'])
def recommend():
    # Get form data
    age = request.form.get('age')
    author = request.form.get('author')
    recent_books = request.form.get('recent_books')
    reading_level = request.form.get('activity_level')

    # Reading level translation
    reading_level_es = {
        'Beginner': 'principiante',
        'Intermediate': 'intermedio',
        'Advanced': 'avanzado'
    }[reading_level]

    # Construct prompt in Spanish
    prompt = f"""Como experto literario, recomienda un libro de {genre} para un lector de nivel {reading_level_es}. 
    Le gustan autores como {author} y ha leído recientemente: {recent_books}. 
    Por favor, proporciona una recomendación que incluya:
    - Título y autor
    - Breve sinopsis
    - Por qué coincide con sus intereses
    - Por qué es adecuado para su nivel de lectura
    Mantén la respuesta concisa pero informativa."""

    print("Prompt que vamos a enviar a Groq:")
    print("-----------------------------")
    print(prompt)
    print("-----------------------------")

    try:
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="mistral-saba-24b",
            temperature=0.7,
            max_tokens=1000,
        )
        
        recommendation = completion.choices[0].message.content
        return jsonify({'success': True, 'recommendation': recommendation})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
