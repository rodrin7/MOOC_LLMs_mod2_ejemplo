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
    edades = [
    '1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33',
    '34','35','36','37','38','39','40','41','42','43','44','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59','60','61','62','63','64',
    '65','66','67','68','69','70','71','72','73','74','75','76','77','78','79','80','81','82','83','84','85','86','87','88','89','90','91','92','93','94','95',
    '96','97','98','99'
    ]
    return render_template('index.html', edad=edad)

@app.route('/recommend', methods=['POST'])
def recommend():
    # Get form data
    edad = request.form.get('edad')
    comdias_favoritas = request.form.get('comidas_favoritas')
    restricciones = request.form.get('rectricciones')
    nivel_actividad = request.form.get('nivel_actividad')

   # Niveles de actividad
    nivele_actividad = [
        ('sedentario', 'Sedentario (Poco o ningún ejercicio)'),
        ('poco_activo', 'Poco Activo (1-3 días/semana)'),
        ('moderadamente_activo', 'Moderadamente Activo (3-5 días/semana)'),
        ('muy_activo', 'Muy Activo (6-7 días/semana)'),
        ('super_activo', 'Super Activo (Atleta profesional/2x entrenamientos)')
    ]

    # Construct prompt in Spanish
    prompt = """Como nutricionista profesional, crea un plan de nutrición personalizado para alguien con el siguiente perfil:
        Edad: {edad} años
        Nivel de Actividad: {nivel_actividad}
        Comidas Favoritas: {comidas_favoritas}
        Restricciones Dietéticas/Alergias: {restricciones}
        Por favor, proporciona:
        1. Estimación de necesidades calóricas diarias
        2. Distribución recomendada de macronutrientes
        3. Un plan de comidas diario de ejemplo incorporando sus comidas favoritas cuando sea posible
        4. Consideraciones nutricionales específicas para su grupo de edad
        5. Recomendaciones basadas en su nivel de actividad
        6. Alternativas seguras para cualquier alimento restringido
        7. 2-3 sugerencias de snacks saludables
        Formatea la respuesta claramente con encabezados y puntos para facilitar la lectura.
        Ten en cuenta la salud y la seguridad, especialmente con respecto a las restricciones mencionadas."""

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
