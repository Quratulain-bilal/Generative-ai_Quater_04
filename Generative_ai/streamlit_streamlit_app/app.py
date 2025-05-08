import streamlit as st
import pandas as pd
import plotly.express as px

# App config
st.set_page_config(
    page_title="Generative AI Explorer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="auto"
)

# Custom CSS with Tailwind CDN and mobile responsiveness
st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
<style>
    .stApp {
        background-color: #f5f5f5;
    }
    .section {
        @apply bg-white rounded-lg p-6 mb-6 shadow-md hover:shadow-lg transition-shadow duration-300 w-full;
    }
    .model-card {
        @apply border-l-4 border-blue-500 pl-4;
    }
    .quiz-question {
        @apply font-bold text-gray-800 text-lg;
    }
    .correct-answer {
        @apply text-green-600 font-semibold;
    }
    .incorrect-answer {
        @apply text-red-600 font-semibold;
    }
    .game-container {
        @apply bg-gray-100 p-6 rounded-lg;
    }
    .sidebar .sidebar-content {
        @apply bg-gray-800 text-white p-4;
    }
    .btn-primary {
        @apply bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors;
    }
    img {
        @apply w-full h-auto rounded-lg;
    }
    /* Mobile-specific styles */
    @media (max-width: 640px) {
        .section {
            padding: 1rem;
        }
        .text-4xl {
            font-size: 1.5rem;
        }
        .text-3xl {
            font-size: 1.25rem;
        }
        .text-2xl {
            font-size: 1rem;
        }
        .text-lg {
            font-size: 0.9rem;
        }
        .text-base {
            font-size: 0.85rem;
        }
        .btn-primary {
            padding: 0.5rem 1rem;
            font-size: 0.9rem;
        }
        img {
            width: 100% !important;
            height: auto !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Sample data
MODELS = {
    "GAN": {
        "description": "Generative Adversarial Networks use two neural networks (generator and discriminator) competing against each other to produce realistic data.",
        "inventor": "Ian Goodfellow (2014)",
        "use_cases": ["Image generation", "Style transfer", "Data augmentation"],
        "examples": ["StyleGAN (NVIDIA)", "CycleGAN", "BigGAN"],
        "image": "https://images.unsplash.com/photo-1618005198919-d3d4b3a0f6c7?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
    },
    "VAE": {
        "description": "Variational Autoencoders learn compressed representations of data and can generate new samples from a latent space.",
        "inventor": "Kingma & Welling (2013)",
        "use_cases": ["Image generation", "Anomaly detection", "Dimensionality reduction"],
        "examples": ["Beta-VAE", "VQ-VAE"],
        "image": "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
    },
    "Transformer": {
        "description": "Attention-based architecture that processes sequential data in parallel, excelling in tasks like text generation.",
        "inventor": "Vaswani et al. (2017)",
        "use_cases": ["Text generation", "Translation", "Summarization"],
        "examples": ["Grok 3 (xAI)", "BERT", "T5"],
        "image": "https://images.unsplash.com/photo-1633356122544-f1347c4d9a9b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
    },
    "Diffusion": {
        "description": "Models that gradually denoise data to generate high-quality samples, known for photorealistic outputs.",
        "inventor": "Sohl-Dickstein et al. (2015)",
        "use_cases": ["Image generation", "Audio synthesis", "Video generation"],
        "examples": ["Stable Diffusion", "DALL-E 2", "Imagen"],
        "image": "https://images.unsplash.com/photo-1657214059233-5626b35a6a04?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
    }
}

COURSES = [
    {
        "name": "Generative AI with LLMs",
        "platform": "Coursera",
        "rating": "4.8/5",
        "duration": "16 hours",
        "link": "https://www.coursera.org/learn/generative-ai-with-llms"
    },
    {
        "name": "DeepLearning.AI Generative AI",
        "platform": "Coursera",
        "rating": "4.9/5",
        "duration": "1 month",
        "link": "https://www.coursera.org/specializations/generative-ai"
    },
    {
        "name": "Generative AI for Beginners",
        "platform": "Udemy",
        "rating": "4.6/5",
        "duration": "11 hours",
        "link": "https://www.udemy.com/course/generative-ai-for-beginners/"
    },
    {
        "name": "Advanced AI: Transformers",
        "platform": "Udemy",
        "rating": "4.7/5",
        "duration": "14 hours",
        "link": "https://www.udemy.com/course/advanced-ai-transformers/"
    }
]

PANAVERSITY_VIDEOS = [
    {
        "title": "Introduction to Generative AI",
        "channel": "Panaversity",
        "url": "https://www.youtube.com/watch?v=G2fqAlgmoPo",
        "thumbnail": "https://i.ytimg.com/vi/G2fqAlgmoPo/hqdefault.jpg"
    },
    {
        "title": "Generative AI Models Explained",
        "channel": "Panaversity",
        "url": "https://www.youtube.com/watch?v=1CIpzeNxIhU",
        "thumbnail": "https://i.ytimg.com/vi/1CIpzeNxIhU/hqdefault.jpg"
    },
    {
        "title": "Real-world Applications of Gen AI",
        "channel": "Panaversity",
        "url": "https://www.youtube.com/watch?v=0LAnm0xYt2s",
        "thumbnail": "https://i.ytimg.com/vi/0LAnm0xYt2s/hqdefault.jpg"
    },
    {
        "title": "Prompt Engineering Masterclass",
        "channel": "Panaversity",
        "url": "https://www.youtube.com/watch?v=xyz123",
        "thumbnail": "https://i.ytimg.com/vi/xyz123/hqdefault.jpg"
    },
    {
        "title": "Future of Generative AI",
        "channel": "Panaversity",
        "url": "https://www.youtube.com/watch?v=abc456",
        "thumbnail": "https://i.ytimg.com/vi/abc456/hqdefault.jpg"
    }
]

QUIZZES = [
    {"question": "What does GAN stand for?", "options": ["Generative Adversarial Network", "Generalized Artificial Neuron", "Graphical Analysis Network", "Generative Algorithmic Network"], "answer": 0},
    {"question": "Which model uses an encoder-decoder architecture?", "options": ["GAN", "VAE", "Transformer", "Diffusion"], "answer": 1},
    {"question": "What year was the Transformer introduced?", "options": ["2015", "2017", "2019", "2021"], "answer": 1},
    {"question": "Which model is best for photorealistic images?", "options": ["GAN", "VAE", "Transformer", "Diffusion"], "answer": 3},
    {"question": "Who invented GANs?", "options": ["Ian Goodfellow", "Yann LeCun", "Geoffrey Hinton", "Andrew Ng"], "answer": 0},
    {"question": "What is a key component of Transformers?", "options": ["Self-attention", "Convolution", "Recurrent layers", "Pooling"], "answer": 0},
    {"question": "Which model uses a latent space?", "options": ["GAN", "VAE", "Transformer", "Diffusion"], "answer": 1},
    {"question": "What is Stable Diffusion's primary use?", "options": ["Text generation", "Image generation", "Code generation", "Audio synthesis"], "answer": 1},
    {"question": "Which company developed Grok 3?", "options": ["OpenAI", "Google", "xAI", "Anthropic"], "answer": 2},
    {"question": "What does VAE stand for?", "options": ["Variable Autoencoder", "Variational Autoencoder", "Vector Autoencoder", "Visual Autoencoder"], "answer": 1},
    {"question": "Which model powers ChatGPT?", "options": ["GAN", "VAE", "Transformer", "Diffusion"], "answer": 2},
    {"question": "What is a discriminator in GANs?", "options": ["Generates data", "Classifies real vs fake", "Encodes data", "Decodes data"], "answer": 1},
    {"question": "Which model adds noise during training?", "options": ["GAN", "VAE", "Transformer", "Diffusion"], "answer": 3},
    {"question": "What is a common Transformer application?", "options": ["Image classification", "Text translation", "Anomaly detection", "Data augmentation"], "answer": 1},
    {"question": "Which model is used in StyleGAN?", "options": ["GAN", "VAE", "Transformer", "Diffusion"], "answer": 0},
    {"question": "What is the generator's role in GANs?", "options": ["Classifies data", "Creates synthetic data", "Encodes data", "Denoises data"], "answer": 1},
    {"question": "Which model powers DALL-E 2?", "options": ["GAN", "VAE", "Transformer", "Diffusion"], "answer": 3},
    {"question": "What is a challenge in training GANs?", "options": ["Overfitting", "Mode collapse", "Underfitting", "High latency"], "answer": 1},
    {"question": "Which model is best for text generation?", "options": ["GAN", "VAE", "Transformer", "Diffusion"], "answer": 2},
    {"question": "What is the goal of prompt engineering?", "options": ["Optimize hardware", "Craft effective inputs", "Train models", "Debug code"], "answer": 1},
    {"question": "Which industry uses AI for drug discovery?", "options": ["Finance", "Healthcare", "Retail", "Education"], "answer": 1},
    {"question": "What is a benefit of VAEs?", "options": ["High-quality images", "Smooth latent space", "Fast training", "Low memory"], "answer": 1},
    {"question": "Which model powers GitHub Copilot?", "options": ["GAN", "VAE", "Transformer", "Diffusion"], "answer": 2},
    {"question": "What is a use case for diffusion models?", "options": ["Text summarization", "Image generation", "Code debugging", "Speech recognition"], "answer": 1},
    {"question": "Who introduced VAEs?", "options": ["Ian Goodfellow", "Kingma & Welling", "Vaswani et al.", "Sohl-Dickstein"], "answer": 1},
    {"question": "What is a feature of diffusion models?", "options": ["Adversarial training", "Latent space", "Denoising process", "Attention mechanism"], "answer": 2},
    {"question": "Which model is used in BERT?", "options": ["GAN", "VAE", "Transformer", "Diffusion"], "answer": 2},
    {"question": "What is a challenge in prompt engineering?", "options": ["Hardware cost", "Ambiguous outputs", "Slow training", "Data scarcity"], "answer": 1},
    {"question": "Which region leads in AI research?", "options": ["Africa", "Asia", "North America", "South America"], "answer": 2},
    {"question": "What is self-attention in Transformers?", "options": ["Reduce parameters", "Weight input importance", "Add noise", "Compress data"], "answer": 1}
]

# Sidebar with navigation
with st.sidebar:
    st.markdown('<div class="p-4"><h1 class="text-2xl font-bold">🔮 GenAI Explorer</h1><p class="text-sm">Explore the world of Generative AI</p></div>', unsafe_allow_html=True)
    menu = st.radio("Navigate to:", [
        "🏠 Home", 
        "🧠 Models", 
        "🌍 Global Usage", 
        "🛠️ Prompt Engineering", 
        "🔬 Research", 
        "💼 Careers",
        "🎓 Courses", 
        "🎥 Videos",
        "📝 Quizzes"
    ])
    st.markdown('<hr class="my-4"><p class="text-center text-sm">Built with ❤️ using Streamlit</p>', unsafe_allow_html=True)

# Home Page
if menu == "🏠 Home":
    st.markdown('<h1 class="text-4xl font-bold text-center mb-6">Generative AI Explorer</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div class="section">
        <h3 class="text-2xl font-semibold">Welcome to the Generative AI Explorer!</h3>
        <p class="text-lg">This interactive app helps you learn about Generative AI through:</p>
        <ul class="list-disc pl-6">
            <li>📚 Comprehensive explanations of different models</li>
            <li>🌍 Global usage patterns and adoption</li>
            <li>🛠️ Prompt engineering techniques</li>
            <li>🔬 Cutting-edge research experiments</li>
            <li>💼 Career opportunities in GenAI</li>
            <li>🎓 Recommended learning resources</li>
        </ul>
        <p class="text-base">Use the sidebar to navigate between sections.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="medium")
    
    with col1:
        st.markdown("""
        <div class="section">
            <h4 class="text-xl font-semibold">What is Generative AI?</h4>
            <p class="text-base">Generative AI is a branch of artificial intelligence that focuses on creating new content, such as text, images, audio, or 3D models, by learning patterns from existing data. Unlike discriminative models that classify or predict, generative models produce novel outputs that resemble the training data's distribution.</p>
            <p class="text-base">Technically, these models learn to sample from complex probability distributions. Key approaches include:</p>
            <ul class="list-disc pl-6">
                <li><strong>GANs:</strong> Use adversarial training with a generator and discriminator.</li>
                <li><strong>VAEs:</strong> Encode data into a latent space for smooth generation.</li>
                <li><strong>Transformers:</strong> Leverage attention mechanisms for sequential data.</li>
                <li><strong>Diffusion Models:</strong> Denoise random inputs to produce high-quality outputs.</li>
            </ul>
            <p class="text-base">Since the introduction of GANs in 2014 by Ian Goodfellow, Generative AI has seen milestones like the Transformer (2017), GPT-3 (2020), and Stable Diffusion (2022). It powers applications from chatbots (e.g., Grok 3 by xAI) to AI art, with a market projected to reach $100B by 2026.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="section">
            <h4 class="text-xl font-semibold">Key Applications</h4>
            <ul class="list-disc pl-6">
                <li>Text generation (ChatGPT, Grok 3)</li>
                <li>Image creation (DALL-E, Stable Diffusion)</li>
                <li>Code generation (GitHub Copilot)</li>
                <li>Music composition (Jukebox)</li>
                <li>Video synthesis (Runway ML)</li>
                <li>3D model generation</li>
                <li>Drug discovery</li>
                <li>Scientific research</li>
            </ul>
            
            <h4 class="text-xl font-semibold mt-4">Quick Facts</h4>
            <div class="model-card">
                <p><strong>2014:</strong> First GAN introduced by Ian Goodfellow</p>
                <p><strong>2017:</strong> Transformer architecture published</p>
                <p><strong>2020:</strong> GPT-3 released with 175B parameters</p>
                <p><strong>2022:</strong> Stable Diffusion makes AI art accessible</p>
                <p><strong>2023:</strong> ChatGPT reaches 100M users in 2 months</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Models Page
elif menu == "🧠 Models":
    st.markdown('<h1 class="text-3xl font-bold mb-6">Generative AI Models</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div class="section">
        <p class="text-base">Explore the different types of generative models and how they work.</p>
    </div>
    """, unsafe_allow_html=True)
    
    selected_model = st.selectbox("Select a model type to learn about:", list(MODELS.keys()))
    
    model_data = MODELS[selected_model]
    
    st.markdown(f"""
    <div class="section">
        <div class="model-card">
            <h3 class="text-2xl font-semibold">{selected_model}</h3>
            <p class="text-base">{model_data['description']}</p>
            <p><strong>Inventor:</strong> {model_data['inventor']}</p>
            
            <h4 class="text-lg font-semibold">Use Cases:</h4>
            <ul class="list-disc pl-6">
                {''.join([f'<li>{uc}</li>' for uc in model_data['use_cases']])}
            </ul>
            
            <h4 class="text-lg font-semibold">Examples:</h4>
            <ul class="list-disc pl-6">
                {''.join([f'<li>{ex}</li>' for ex in model_data['examples']])}
            </ul>
            
            <h4 class="text-lg font-semibold">Technical Details:</h4>
        </div>
        <img src="{model_data['image']}" alt="{selected_model} illustration">
    </div>
    """, unsafe_allow_html=True)
    
    if selected_model == "GAN":
        st.markdown("""
        <div class="section">
            <p>GANs consist of two neural networks:</p>
            <ul class="list-disc pl-6">
                <li><strong>Generator:</strong> Creates synthetic data from random noise</li>
                <li><strong>Discriminator:</strong> Distinguishes real from generated data</li>
            </ul>
            <p>They are trained adversarially - the generator improves to fool the discriminator, 
            while the discriminator improves at detecting fakes.</p>
        </div>
        """, unsafe_allow_html=True)
    elif selected_model == "VAE":
        st.markdown("""
        <div class="section">
            <p>VAEs consist of:</p>
            <ul class="list-disc pl-6">
                <li><strong>Encoder:</strong> Maps input to a latent space distribution</li>
                <li><strong>Decoder:</strong> Reconstructs data from latent space samples</li>
            </ul>
            <p>They learn a compressed representation while regularizing the latent space 
            to enable smooth interpolation and generation.</p>
        </div>
        """, unsafe_allow_html=True)
    elif selected_model == "Transformer":
        st.markdown("""
        <div class="section">
            <p>Key components:</p>
            <ul class="list-disc pl-6">
                <li><strong>Self-attention:</strong> Weights importance of different input parts</li>
                <li><strong>Positional encoding:</strong> Captures sequence order information</li>
                <li><strong>Feed-forward networks:</strong> Processes attention outputs</li>
            </ul>
            <p>Transformers process all tokens in parallel (unlike RNNs) and can model 
            long-range dependencies effectively.</p>
        </div>
        """, unsafe_allow_html=True)
    elif selected_model == "Diffusion":
        st.markdown("""
        <div class="section">
            <p>Diffusion models work by:</p>
            <ul class="list-disc pl-6">
                <li><strong>Forward process:</strong> Gradually adds Gaussian noise to data</li>
                <li><strong>Reverse process:</strong> Learns to denoise through neural network</li>
            </ul>
            <p>At inference time, they generate data by iteratively denoising random noise.</p>
        </div>
        """, unsafe_allow_html=True)

# Global Usage Page
elif menu == "🌍 Global Usage":
    st.markdown('<h1 class="text-3xl font-bold mb-6">Global Adoption of Generative AI</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div class="section">
        <h3 class="text-2xl font-semibold">How Generative AI is Being Used Worldwide</h3>
        <p class="text-base">Explore how different industries and regions are adopting generative AI technologies.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # World Map
    df = pd.DataFrame({
        'Country': ['USA', 'China', 'Germany', 'India', 'Brazil', 'South Africa'],
        'Adoption': [80, 70, 65, 60, 50, 45]
    })
    fig = px.choropleth(df, locations="Country", locationmode="country names", color="Adoption",
                        hover_name="Country", color_continuous_scale=px.colors.sequential.Plasma,
                        title="Global AI Adoption (Sample Data)")
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns([1, 1], gap="medium")
    
    with col1:
        st.markdown("""
        <div class="section">
            <h4 class="text-xl font-semibold">By Industry</h4>
            <ul class="list-disc pl-6">
                <li><strong>Technology:</strong> Code generation, documentation, debugging</li>
                <li><strong>Healthcare:</strong> Drug discovery, medical imaging analysis</li>
                <li><strong>Finance:</strong> Fraud detection, risk assessment, report generation</li>
                <li><strong>Education:</strong> Personalized learning, content creation</li>
                <li><strong>Marketing:</strong> Ad copy, personalized content, SEO optimization</li>
                <li><strong>Entertainment:</strong> Script writing, game assets, music composition</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="section">
            <h4 class="text-xl font-semibold">By Region</h4>
            <ul class="list-disc pl-6">
                <li><strong>North America:</strong> Leading in AI research and enterprise adoption</li>
                <li><strong>Europe:</strong> Strong in ethical AI frameworks and creative applications</li>
                <li><strong>Asia:</strong> Rapid adoption in manufacturing and customer service</li>
                <li><strong>Middle East:</strong> Government-led initiatives in Arabic NLP</li>
                <li><strong>Africa:</strong> Emerging use cases in agriculture and healthcare</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="section">
        <h4 class="text-xl font-semibold">Adoption Statistics</h4>
        <ul class="list-disc pl-6">
            <li>60% of enterprises are piloting or using generative AI (2023)</li>
            <li>40% of organizations plan to increase AI investment</li>
            <li>Top use cases: Content creation (35%), customer service (28%), code generation (24%)</li>
            <li>Most adopted tools: ChatGPT (55%), Bard (22%), Claude (15%)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="section">
        <h4 class="text-xl font-semibold">Case Studies</h4>
        <div class="model-card">
            <p><strong>Healthcare:</strong> Mayo Clinic using generative AI for clinical note summarization</p>
            <p><strong>Finance:</strong> Morgan Stanley's AI assistant for financial advisors</p>
            <p><strong>Retail:</strong> Shopify's AI shopping assistant</p>
            <p><strong>Manufacturing:</strong> Siemens using AI for industrial design optimization</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Prompt Engineering Page
elif menu == "🛠️ Prompt Engineering":
    st.markdown('<h1 class="text-3xl font-bold mb-6">Prompt Engineering Guide</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div class="section">
        <h3 class="text-2xl font-semibold">Mastering the Art of Prompting</h3>
        <p class="text-base">Learn how to craft effective prompts for different generative AI systems.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="section">
        <h4 class="text-xl font-semibold">Fundamentals of Prompt Engineering</h4>
        <ul class="list-disc pl-6">
            <li><strong>Be specific:</strong> Clearly define what you want</li>
            <li><strong>Provide context:</strong> Give relevant background information</li>
            <li><strong>Use examples:</strong> Show the format you want</li>
            <li><strong>Iterate:</strong> Refine prompts based on outputs</li>
            <li><strong>Chain prompts:</strong> Break complex tasks into steps</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Text", "Code", "Images"])
    
    with tab1:
        st.markdown("""
        <div class="section">
            <h4 class="text-lg font-semibold">Text Generation Prompts</h4>
            <p><strong>Basic:</strong> "Explain quantum computing in simple terms"</p>
            <p><strong>Advanced:</strong> "Write a 300-word blog post about renewable energy trends in 2023, 
            targeting business executives, with a professional tone and 3 key takeaways"</p>
            <p><strong>Structured:</strong> "Create a comparison table of Python vs R for data science with 
            columns for: ease of learning, library ecosystem, performance, and visualization capabilities"</p>
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("""
        <div class="section">
            <h4 class="text-lg font-semibold">Code Generation Prompts</h4>
            <p><strong>Basic:</strong> "Write a Python function to calculate factorial"</p>
            <p><strong>Advanced:</strong> "Create a Flask API endpoint that accepts JSON input with 'name' and 
            'email' fields, validates the email format, and stores the data in a SQLite database"</p>
            <p><strong>Debugging:</strong> "Here's my Python code that's giving an IndexError: [code snippet]. 
            Explain the error and fix it"</p>
        </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("""
        <div class="section">
            <h4 class="text-lg font-semibold">Image Generation Prompts</h4>
            <p><strong>Basic:</strong> "A red apple on a wooden table"</p>
            <p><strong>Advanced:</strong> "A futuristic cityscape at sunset, cyberpunk style, neon lights, 
            raining, highly detailed, 8k resolution, cinematic lighting"</p>
            <p><strong>Artistic:</strong> "A portrait of a robot in the style of Van Gogh, thick brushstrokes, 
            vibrant colors, post-impressionist style"</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="section">
        <h4 class="text-xl font-semibold">Advanced Techniques</h4>
        <ul class="list-disc pl-6">
            <li><strong>Few-shot learning:</strong> Provide examples of desired output</li>
            <li><strong>Chain-of-thought:</strong> Ask the model to think step by step</li>
            <li><strong>Persona pattern:</strong> Assign a role to the AI ("Act as...")</li>
            <li><strong>Template pattern:</strong> Define a strict output format</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Research Page
elif menu == "🔬 Research":
    st.markdown('<h1 class="text-3xl font-bold mb-6">Generative AI Research Frontiers</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div class="section">
        <h3 class="text-2xl font-semibold">Cutting-edge Research in Generative AI</h3>
        <p class="text-base">Explore the latest breakthroughs and experimental applications of generative AI.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="section">
        <h4 class="text-xl font-semibold">Recent Breakthroughs (2023-2024)</h4>
        <ul class="list-disc pl-6">
            <li><strong>Multimodal models:</strong> Systems that can process and generate across text, images, audio</li>
            <li><strong>Long-context models:</strong> Handling of 1M+ token contexts (Google Gemini)</li>
            <li><strong>Agentic systems:</strong> AI that can plan and execute multi-step tasks</li>
            <li><strong>Efficiency improvements:</strong> Techniques to reduce compute requirements</li>
            <li><strong>Controllable generation:</strong> Better steering of model outputs</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="medium")
    
    with col1:
        st.markdown("""
        <div class="section">
            <h4 class="text-xl font-semibold">Notable Research Papers</h4>
            <ul class="list-disc pl-6">
                <li>"Attention Is All You Need" (Transformer paper)</li>
                <li>"Denoising Diffusion Probabilistic Models"</li>
                <li>"Language Models are Few-Shot Learners" (GPT-3)</li>
                <li>"Hierarchical Text-Conditional Image Generation" (DALL-E 2)</li>
                <li>"LLaMA: Open and Efficient Foundation Language Models"</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="section">
            <h4 class="text-xl font-semibold">Emerging Applications</h4>
            <ul class="list-disc pl-6">
                <li>Protein/DNA sequence generation for drug discovery</li>
                <li>Generative AI for scientific hypothesis generation</li>
                <li>AI-generated virtual worlds and environments</li>
                <li>Personalized education content generation</li>
                <li>Automated legal document drafting</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="section">
        <h4 class="text-xl font-semibold">Major Research Labs</h4>
        <div class="model-card">
            <p><strong>OpenAI:</strong> GPT series, DALL-E, Codex</p>
            <p><strong>Google DeepMind:</strong> Gemini, AlphaFold, Imagen</p>
            <p><strong>Anthropic:</strong> Claude models, Constitutional AI</p>
            <p><strong>Meta:</strong> LLaMA, AudioCraft, ImageBind</p>
            <p><strong>Stability AI:</strong> Stable Diffusion, StableLM</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Careers Page
elif menu == "💼 Careers":
    st.markdown('<h1 class="text-3xl font-bold mb-6">Generative AI Career Guide</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div class="section">
        <h3 class="text-2xl font-semibold">Building a Career in Generative AI</h3>
        <p class="text-base">Explore job opportunities and skill development paths in the generative AI field.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="section">
        <h4 class="text-xl font-semibold">Key Job Roles</h4>
        <ul class="list-disc pl-6">
            <li><strong>Prompt Engineer:</strong> Specializes in crafting effective AI prompts</li>
            <li><strong>AI Research Scientist:</strong> Develops new models and algorithms</li>
            <li><strong>ML Engineer:</strong> Implements and deploys generative models</li>
            <li><strong>AI Product Manager:</strong> Leads generative AI product development</li>
            <li><strong>Data Scientist:</strong> Applies generative AI to business problems</li>
            <li><strong>AI Ethics Specialist:</strong> Ensures responsible AI development</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="medium")
    
    with col1:
        st.markdown("""
        <div class="section">
            <h4 class="text-xl font-semibold">Required Skills</h4>
            <ul class="list-disc pl-6">
                <li>Machine learning fundamentals</li>
                <li>Deep learning architectures</li>
                <li>Natural language processing</li>
                <li>Python programming</li>
                <li>Cloud computing platforms</li>
                <li>Prompt engineering</li>
                <li>Data visualization</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="section">
            <h4 class="text-xl font-semibold">Salary Ranges (US)</h4>
            <ul class="list-disc pl-6">
                <li>Prompt Engineer: $90k-$150k</li>
                <li>AI Research Scientist: $120k-$250k</li>
                <li>ML Engineer: $110k-$200k</li>
                <li>AI Product Manager: $130k-$220k</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="section">
        <h4 class="text-xl font-semibold">Career Development Path</h4>
        <ol class="list-decimal pl-6">
            <li>Learn fundamentals through courses and certifications</li>
            <li>Build projects showcasing generative AI applications</li>
            <li>Contribute to open-source AI projects</li>
            <li>Specialize in a domain (NLP, computer vision, etc.)</li>
            <li>Stay updated with latest research and tools</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

# Courses Page
elif menu == "🎓 Courses":
    st.markdown('<h1 class="text-3xl font-bold mb-6">Recommended Courses</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div class="section">
        <p class="text-base">Explore these high-quality courses to deepen your Generative AI knowledge.</p>
    </div>
    """, unsafe_allow_html=True)
    
    for course in COURSES:
        st.markdown(f"""
        <div class="section">
            <h4 class="text-lg font-semibold"><a href="{course['link']}" target="_blank">{course['name']}</a></h4>
            <p><strong>Platform:</strong> {course['platform']} | <strong>Rating:</strong> {course['rating']} | <strong>Duration:</strong> {course['duration']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="section">
        <h4 class="text-xl font-semibold">Other Learning Resources</h4>
        <ul class="list-disc pl-6">
            <li><a href="https://developers.google.com/machine-learning/generative-ai" target="_blank">Google's Generative AI Learning Path</a></ lions>
            <li><a href="https://huggingface.co/course" target="_blank">HuggingFace NLP Course</a></li>
            <li><a href="https://www.fast.ai/" target="_blank">Practical Deep Learning (fast.ai)</a></li>
            <li><a href="https://www.deeplearning.ai/short-courses/" target="_blank">DeepLearning.AI Short Courses</a></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Videos Page
elif menu == "🎥 Videos":
    st.markdown('<h1 class="text-3xl font-bold mb-6">Educational Videos</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div class="section">
        <p class="text-base">Watch these informative videos about Generative AI from trusted sources.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Panaversity Generative AI Videos")
    cols = st.columns([1, 1, 1], gap="medium")
    for i, video in enumerate(PANAVERSITY_VIDEOS):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="section">
                <img src="{video['thumbnail']}" alt="{video['title']}">
                <h5 class="text-base font-semibold">{video['title']}</h5>
                <p>{video['channel']}</p>
                <a href="{video['url']}" class="btn-primary" target="_blank">Watch Video</a>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="section">
        <h4 class="text-xl font-semibold">More Video Resources</h4>
        <ul class="list-disc pl-6">
            <li><a href="https://www.youtube.com/@DeepLearningAI" target="_blank">DeepLearning.AI</a></li>
            <li><a href="https://www.youtube.com/@TwoMinutePapers" target="_blank">Two Minute Papers</a></li>
            <li><a href="https://www.youtube.com/@YannicKilcher" target="_blank">Yannic Kilcher</a></li>
            <li><a href="https://www.youtube.com/@GoogleCloudTech" target="_blank">Google Cloud Tech</a></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Quizzes Page
elif menu == "📝 Quizzes":
    st.markdown('<h1 class="text-3xl font-bold mb-6">Test Your Knowledge</h1>', unsafe_allow_html=True)
    st.markdown('<div class="section"><p class="text-base">Take a quiz to test your understanding of Generative AI.</p></div>', unsafe_allow_html=True)
    
    if 'quiz_state' not in st.session_state:
        st.session_state.quiz_state = {
            'current': 0,
            'score': 0,
            'answered': False,
            'selected': None
        }

    quiz = QUIZZES[st.session_state.quiz_state['current']]
    st.markdown(f'<div class="section quiz-question">{quiz["question"]}</div>', unsafe_allow_html=True)
    
    for i, option in enumerate(quiz['options']):
        if st.button(option, key=f"option_{i}"):
            if not st.session_state.quiz_state['answered']:
                st.session_state.quiz_state['selected'] = i
                st.session_state.quiz_state['answered'] = True
                if i == quiz['answer']:
                    st.session_state.quiz_state['score'] += 1
                    st.markdown('<p class="correct-answer">Correct!</p>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<p class="incorrect-answer">Incorrect. The correct answer is {quiz["options"][quiz["answer"]]}</p>', unsafe_allow_html=True)

    if st.session_state.quiz_state['answered'] and st.button("Next Question", key="next_question"):
        st.session_state.quiz_state['current'] += 1
        st.session_state.quiz_state['answered'] = False
        st.session_state.quiz_state['selected'] = Ditto
        if st.session_state.quiz_state['current'] >= len(QUIZZES):
            st.markdown(f'<div class="section"><h3 class="text-2xl font-semibold">Quiz Complete!</h3><p class="text-base">Your score: {st.session_state.quiz_state["score"]}/{len(QUIZZES)}</p></div>', unsafe_allow_html=True)
            st.session_state.quiz_state['current'] = 0
            st.session_state.quiz_state['score'] = 0

# Footer
st.markdown("""
<hr class="my-6">
<div class="text-center text-gray-700 py-4">
    <p>Generative AI Explorer | Built with Streamlit</p>
    <p>© 2023 All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)
