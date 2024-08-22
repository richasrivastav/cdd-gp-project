import streamlit as st
from PIL import Image
import numpy as np
import tensorflow as tf
# import os

# Path to your model file
MODEL_PATH = 'C:/Users/DELL/Desktop/ONLY OJT/gpt project/your_model_name.h5'

def load_model():
    if not os.path.exists(MODEL_PATH):
        st.error(f"Model file not found at path: {MODEL_PATH}")
        return None
    try:
        model = tf.keras.models.load_model(MODEL_PATH)
        return model
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

# Load your model
model = load_model()

# Define a dictionary to map disease classes to solutions
disease_solutions = {
    'Healthy': 'No treatment needed. Keep monitoring the crop regularly.',
    'Leaf Blast': (
        '1. **Chemical Treatment:** Apply fungicides such as Pyricularia or Propiconazole. '
        '2. **Cultural Practices:** Improve irrigation management to avoid excessive moisture. '
        '3. **Resistant Varieties:** Use rice varieties resistant to Leaf Blast. '
        '4. **Home Remedy:** Spray a mixture of water and garlic (1 bulb per liter) to help deter fungal growth.'
    ),
    'Brown Spot': (
        '1. **Chemical Treatment:** Use fungicides like Carbendazim or Mancozeb. '
        '2. **Fertilization:** Ensure proper application of nutrients, especially nitrogen. '
        '3. **Resistant Varieties:** Choose rice varieties that are less susceptible to Brown Spot. '
        '4. **Home Remedy:** Mix neem oil with water (1 tablespoon per liter) and spray on affected leaves to reduce fungal spread.'
    ),
    'Sheath Blight': (
        '1. **Chemical Treatment:** Apply fungicides such as Tricyclazole or Validamycin. '
        '2. **Water Management:** Maintain optimal water levels and avoid excessive irrigation. '
        '3. **Crop Rotation:** Rotate crops to disrupt the lifecycle of the pathogen. '
        '4. **Home Remedy:** Spray a solution of baking soda (1 teaspoon per liter) to help inhibit fungal growth.'
    )
}

# Function to load and preprocess the image
def load_image(image_file):
    img = Image.open(image_file).convert('RGB')  # Ensure image is in RGB mode
    return img

def predict_disease(img, model):
    if model is None:
        return "Model is not loaded", "Model is not loaded"

    # Preprocess the image to match your model's expected input
    img = img.resize((224, 224))  # Resize to the input size your model expects
    img = np.array(img) / 255.0  # Normalize pixel values
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    
    # Predict using the model
    prediction = model.predict(img)
    class_names = ['Healthy', 'Leaf Blast', 'Brown Spot', 'Sheath Blight']  # Example class names
    predicted_class = class_names[np.argmax(prediction)]
    
    # Get the solution from the dictionary
    solution = disease_solutions.get(predicted_class, 'Solution not available.')
    
    return predicted_class, solution

def chatbot_response(user_input):
    # Simple keyword-based response system
    user_input = user_input.lower()
    
    if 'healthy' in user_input:
        return disease_solutions['Healthy']
    elif 'leaf blast' in user_input:
        return disease_solutions['Leaf Blast']
    elif 'brown spot' in user_input:
        return disease_solutions['Brown Spot']
    elif 'sheath blight' in user_input:
        return disease_solutions['Sheath Blight']
    else:
        return "We are connecting as soon as."

# Custom CSS for styling
st.markdown(
    """
    <style>
    /* General styling */
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f4f4f9;
        margin: 0;
        padding: 0;
    }
    .main {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
    }
    /* Navbar styling */
    .navbar {
        background-color: #2E8B57;
        padding: 15px;
        border-radius: 0 0 10px 10px;
        margin-bottom: 20px;
        display: flex;
        justify-content: center;
    }
    .navbar a {
        color: white;
        text-decoration: none;
        padding: 10px 20px;
        font-size: 18px;
        font-weight: bold;
        display: inline-block;
        margin: 0 10px;
        transition: background-color 0.3s ease;
    }
    .navbar a:hover {
        background-color: #1E693D;
        border-radius: 5px;
    }
    /* Heading styling */
    h1, h2, h3, h4, h5 {
        color: #2E8B57;
        font-family: 'Arial', sans-serif;
    }
    /* Button styling */
    .stButton > button {
        background-color: #2E8B57;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        font-family: 'Arial', sans-serif;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        transition: background-color 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #1E693D;
    }
    /* Image styling */
    img {
        border-radius: 10px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
    }
    /* Container styling */
    .container {
        max-width: 1200px;
        margin: 0 auto;
    }
    /* Section styling */
    .section {
        margin-bottom: 40px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit App Layout
def main():
    st.title("🌱 AI-Powered Crop Disease Detection")
    st.write("""
    Welcome to the **Crop Disease Detection** tool. Upload an image of a crop, and our AI model will predict if the crop is diseased and suggest possible solutions.
    """)
    
    # Create navbar
    st.markdown("""
    <div class="navbar">
        <a href="#home">Home</a>
        <a href="#disease-library">Disease Library</a>
        <a href="#blog">Blog</a>
        <a href="#about-us">About Us</a>
        <a href="#contact">Contact</a>
    </div>
    """, unsafe_allow_html=True)

    menu = ["Home", "Disease Library", "Blog", "About Us", "Contact"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Upload Crop Image")
        st.write("""
        **Upload an image of your crop to check for diseases. Our AI model will analyze the image and provide a diagnosis along with possible solutions.**
        """)
        image_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])
        
        if image_file is not None:
            img = load_image(image_file)
            st.image(img, caption='Uploaded Image', use_column_width=True)
            
            if st.button("Predict"):
                predicted_class, solution = predict_disease(img, model)
                st.success(f"Prediction: {predicted_class}")
                st.write(f"Suggested Solution: {solution}")
    
    elif choice == "Disease Library":
        st.subheader("📚 Crop Disease Library")
        st.write("""
        Explore a comprehensive library of crop diseases. Discover symptoms, causes, and treatments to help keep your crops healthy.
        """)
        st.write("<div class='section'><h3>Leaf Blast</h3></div>", unsafe_allow_html=True)
        st.write("""
        Leaf Blast is a common disease affecting rice crops. Symptoms include large, oval lesions on leaves, which eventually turn grayish-brown.
        **Treatment:** Apply fungicides and improve irrigation management.
        """)
        st.write("<div class='section'><h3>Brown Spot</h3></div>", unsafe_allow_html=True)
        st.write("""
        Brown Spot causes small, brown lesions on leaves. It is often caused by improper fertilization.
        **Treatment:** Use resistant varieties and apply proper fertilizers.
        """)
        st.write("<div class='section'><h3>Sheath Blight</h3></div>", unsafe_allow_html=True)
        st.write("""
        Sheath Blight causes lesions on the sheaths of rice plants. It is often exacerbated by high humidity.
        **Treatment:** Apply fungicides and manage water levels carefully.
        """)
        st.write("<div class='section'><h3>Healthy</h3></div>", unsafe_allow_html=True)
        st.write("""
        The crop is healthy. No treatment needed. Keep monitoring the crop regularly.
        """)

    elif choice == "Blog":
        st.subheader("📝 Blog")
        st.write("""
        **Stay updated with the latest trends and tips in crop management. Our blog covers various topics including disease prevention, treatment options, and best practices for maintaining healthy crops.**
        """)
        st.write("<div class='section'><h3>Understanding Crop Diseases</h3></div>", unsafe_allow_html=True)
        st.write("""
        Crops are susceptible to a range of diseases that can affect yield and quality. Understanding the symptoms and causes of these diseases is crucial for effective management.
        """)
        st.write("<div class='section'><h3>Preventive Measures</h3></div>", unsafe_allow_html=True)
        st.write("""
        Preventing crop diseases involves good agricultural practices such as proper irrigation, fertilization, and the use of resistant crop varieties.
        """)
        st.write("<div class='section'><h3>Latest Research</h3></div>", unsafe_allow_html=True)
        st.write("""
        Our blog features the latest research and innovations in crop disease management. Stay informed about new treatments and technologies.
        """)

    elif choice == "About Us":
        st.subheader("About Us")
        st.write("""
        **We are a team of agricultural scientists and AI experts dedicated to improving crop health through innovative technology. Our goal is to provide farmers with tools and knowledge to manage crop diseases effectively.**
        """)
        st.write("""
        **Our Mission:** To leverage AI and machine learning to provide accurate and actionable insights for crop disease management.
        **Our Vision:** To enhance agricultural productivity and sustainability through advanced technological solutions.
        """)

    elif choice == "Contact":
        st.subheader("Contact Us")
        st.write("""
        **Have any questions or feedback? Reach out to us through the following contact details:**
        """)
        st.write("📧 Email: contact@cropdiseaseapp.com")
        st.write("📞 Phone: +1 (123) 456-7890")
        st.write("""
        **Follow us on social media:**
        - Twitter: [@CropDiseaseApp](https://twitter.com/CropDiseaseApp)
        - Facebook: [CropDiseaseApp](https://facebook.com/CropDiseaseApp)
        """)

if __name__ == "__main__":
    main()

