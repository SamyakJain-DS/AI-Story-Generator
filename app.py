import streamlit as st
from streamlit_autorefresh import st_autorefresh
import time
import numpy as np
from generate_artifacts import *

def create_space(n_lines):
    for i in range(n_lines):
        st.write("")

if "allow_autorefresh" not in st.session_state:
    st.session_state.allow_autorefresh = True

if st.session_state.allow_autorefresh:
    st_autorefresh(interval=2000, key="textbox_placeholder_refresh")

MAX_IMAGES = 8

st.title("AI Story Generator")
st.markdown(
    """
    #### Generate Creative Stories Using AI!
    """
    )

st.markdown("""
<style>
textarea::placeholder {
    font-style: italic;
}
</style>
""", unsafe_allow_html=True)

placeholder_texts = ['Turn the uploaded images into a compelling story...', 'Imagine what happened before and after the moment shown in the images...', 'Write a story that brings the uploaded images to life...', 'Tell a story related to the uploaded images, inspired by real-world events...']

if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

if "story_prompt" not in st.session_state:
    st.session_state.story_prompt = ""

if "story_generated" not in st.session_state:
    st.session_state.story_generated = True

if "generated_story" not in st.session_state:
    st.session_state.generated_story = ""

if "uploaded_images" not in st.session_state:
    st.session_state.uploaded_images = []

elapsed = int(time.time() - st.session_state.start_time)

index = (elapsed // 4) % len(placeholder_texts)

user_prompt = st.text_area("Enter Some Context For Your Story Below! (Optional)", height=100, placeholder=placeholder_texts[index], key='story_prompt')
st.caption("Note: Please only provide relevant context for a story. If the text is irrelevant, it will be ignored.")

st.session_state.uploaded_images = st.file_uploader("Upload Images (Only PNG, JPG, and JPEG formats allowed)", accept_multiple_files=True, type=['png', 'jpeg', 'jpg'])
st.caption(f"Note: Please limit the number of images uploaded to a maximum of {MAX_IMAGES} images.")

if st.session_state.uploaded_images:
    if len(st.session_state.uploaded_images) > MAX_IMAGES:
        st.warning(f"You can only upload up to {MAX_IMAGES} images. Selecting only the first {MAX_IMAGES} images.")
        images = st.session_state.uploaded_images[:MAX_IMAGES]
    cols = st.columns(len(st.session_state.uploaded_images))
    for col, image in zip(cols, st.session_state.uploaded_images):
        with col:
            st.image(image, width=500)

genres = ["Random", "Fantasy", "Science Fiction", "Mystery", "Romance", "Horror", "Comedy", "Thriller"]

st.session_state.genre = st.selectbox("Select A Genre:", genres)

if st.session_state.genre == "Random":
    st.session_state.genre = np.random.choice(genres)

st.session_state.word_limit = st.select_slider("Word Limit", options=[50, 100, 150, 200, 250, 300], value=100)

if "decision" not in st.session_state:
    st.session_state.decision = True

if "generated_story" not in st.session_state:
    st.session_state.generated_story = ""

if "generated_audio" not in st.session_state:
    st.session_state.generated_audio = None

if st.button("Generate Story"):
    st.session_state.allow_autorefresh = False
    with st.spinner("Your Story Is Being Generated..... This May Take A Few Moments."):

        st.session_state.decision, st.session_state.reason = evaluate_story_prompt(st.session_state.story_prompt)
        st.session_state.story_generated, st.session_state.generated_story = generate_story_text(st.session_state.uploaded_images, st.session_state.genre, st.session_state.word_limit, st.session_state.story_prompt)

        if st.session_state.story_generated:
            st.session_state.generated_audio = generate_audio(st.session_state.generated_story)

if not st.session_state.story_generated:
    st.error(st.session_state.generated_story)

if not st.session_state.decision:
    if user_prompt:
        st.caption(f"Note: The provided prompt was not suitable for story generation. Reason: {st.session_state.reason}")

create_space(3)

st.subheader("The Generated Story in Text:")
create_space(1)
st.write(st.session_state.generated_story)

create_space(3)

st.subheader("The Audio File For The Generated Story:")
create_space(1)
st.audio(st.session_state.generated_audio, format="audio/wav")