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
    # Define genres in Spanish
    genres = [
        'Ciencia Ficción', 'Fantasía', 'Misterio', 'Romance', 
        'Ficción Histórica', 'Ficción Literaria', 'Terror',
        'Suspense', 'No Ficción', 'Biografía'
    ]
    return render_template('index.html', genres=genres)

@app.route('/recommend', methods=['POST'])
def recommend():
    # Get form data
    genre = request.form.get('genre')
    author = request.form.get('author')
    recent_books = request.form.get('recent_books')
    reading_level = request.form.get('reading_level')

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
            model="mixtral-8x7b-32768",
            temperature=0.7,
            max_tokens=1000,
        )
        
        recommendation = completion.choices[0].message.content
        return jsonify({'success': True, 'recommendation': recommendation})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)