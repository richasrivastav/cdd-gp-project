import streamlit as st
from PIL import Image
import numpy as np
import tensorflow as tf

# Load your model
model = tf.keras.models.load_model('C:/Users/DELL/Desktop/ONLY OJT/gpt project/your_model_name.h5')

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

def predict_disease(img):
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
        padding: 10px;
        border-radius: 0 0 10px 10px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-around;
    }
    .navbar a {
        color: white;
        text-decoration: none;
        padding: 10px 20px;
        font-size: 16px;
        display: inline-block;
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
        image_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])
        
        if image_file is not None:
            img = load_image(image_file)
            st.image(img, caption='Uploaded Image', use_column_width=True)
            
            if st.button("Predict"):
                predicted_class, solution = predict_disease(img)
                st.success(f"Prediction: {predicted_class}")
                st.write(f"Suggested Solution: {solution}")
    
    elif choice == "Disease Library":
        st.subheader("📚 Crop Disease Library")
        st.write("""
        Explore a comprehensive library of crop diseases. Discover symptoms, causes, and treatments to help keep your crops healthy.
        """)
        st.write("### Leaf Blast")
        st.write("""
        Leaf Blast is a common disease affecting rice crops. Symptoms include large, oval lesions on leaves, which eventually turn grayish-brown.
        **Treatment:** Apply fungicides and improve irrigation management.
        """)
        st.write("### Brown Spot")
        st.write("""
        Brown Spot causes small, brown lesions on leaves. It is often caused by improper fertilization.
        **Treatment:** Use resistant varieties and apply proper fertilizers.
        """)
        st.write("### Sheath Blight")
        st.write("""
        Sheath Blight causes lesions on the sheaths of rice plants. It is often exacerbated by high humidity.
        **Treatment:** Apply fungicides and manage water levels carefully.
        """)
        st.write("### Healthy")
        st.write("""
        The crop is healthy. No treatment needed. Keep monitoring the crop regularly.
        """)

    elif choice == "Blog":
        st.subheader("📝 Educational Blog")
        st.write("""
        Stay updated with the latest articles on crop health, disease management, and new research in agriculture.
        """)
        st.write("### Latest Blog Post")
        st.write("""
        **Title:** Advances in Crop Disease Detection
        **Summary:** Discover the latest technologies and methods used in detecting and managing crop diseases.
        **Read more**: [Link to full article]
        """)

    elif choice == "About Us":
        st.subheader("👩‍🌾 About Us")
        st.write("""
        We are a dedicated team of AI enthusiasts and agricultural experts committed to empowering farmers with innovative tools for crop disease detection and management.
        **Our Mission:** To leverage cutting-edge technology to improve crop health and increase agricultural productivity.
        **Our Team:** Comprised of data scientists, agricultural specialists, and software engineers working together to make a difference.
        """)

    elif choice == "Contact":
        st.subheader("📞 Contact Us")
        st.write("""
        Have any questions? Get in touch with us for support, partnership opportunities, or general inquiries.
        """)
        st.text_input("Name")
        st.text_input("Email")
        st.text_area("Message")
        st.button("Send Message")
        
# Chat input
    user_input = st.text_input("Type your question here:")

    if st.button("Send"):
        response = chatbot_response(user_input)
        st.write(f"**Bot:** {response}")

if __name__ == '__main__':
    main()
