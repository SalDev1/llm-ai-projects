import fitz
import gradio as gr
import os
from dotenv import load_dotenv
from openai import OpenAI
import anthropic

# Setting up the port number and the API keys.
load_dotenv(override=True)
api_key = os.getenv("OPENAI_API_KEY")
anthropic_key = os.getenv("CLAUDE_API_KEY")

# Use the port provided by Elastic Beanstalk.
port = int(os.environ.get("PORT", 8080))

if api_key and api_key.startswith('sk-proj-') and len(api_key)>10:
    print("ChatGPT API key looks good so far")

if anthropic_key and anthropic_key.startswith('sk-ant') and len(anthropic_key)>10:
    print("Claude API key looks good so far")

chatgpt_model = 'gpt-4o-mini'

openai = OpenAI()
claude = anthropic.Anthropic(api_key=anthropic_key)

fetch_content = []
model_selected = ['GPT']

# Fetching all the content inside a pdf, once the user uploads it to the Gradio UI.
# Returns the array of pages from the pdf and open the pdf document.
def summarize_content_pdf(file_path): 
    print("salman file_path is : " , file_path)
    if(hasattr(file_path,'read')):
        # This allows to read the pdf files in the form of bytes , will work in Mobiles.
        doc = fitz.open(stream=file_path.read(), filetype="pdf")
    else : 
        doc = fitz.open(file_path)
    print(type(doc))  # <class 'fitz.fitz.Document'>

    print(doc.page_count)  # Number of pages in the pdf file.

    main_txt = "";
    for page in doc : 
        text = page.get_text()
        main_txt += text

    print(main_txt);
    fetch_content.append(main_txt)


def set_system_message(main_text):
   print('salman main_text is : ' , main_text)
   system_message = f"You are a helpful assistant that summarizes the content of a resume in a concise manner and provide crucial insights. \
    Summarize yourself with the following resume content given to you : {main_text}. \
    If no content is given, politely ask the user to upload a resume file. \
    After summarizing, you are ready to provide your insights on where the candidate is ideal for a specific job role"
   return system_message;

# Chat Function if the user selects the Claude Model.
def chat_fn_chatgpt(message, history):
    # Combining system + history + current message as one every single time the conversation continues.
    messages = [{"role": "system", "content": set_system_message(fetch_content[0] if fetch_content else '')}] + history + [{"role": "user", "content": message}]

    print("History is:")
    print(history)
    print("And messages is:")
    print(messages)

    stream = openai.chat.completions.create(model=chatgpt_model, messages=messages, stream=True)
    return stream;

def chat_fn_claude(message, history):
    result = claude.messages.stream(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        temperature=0.7,
        system=set_system_message(fetch_content[0] if fetch_content else ''), 
        messages=[{"role": "user", "content": message}]
    )
    return result;

def model_chosen(model) : 
    model_selected[0] = model

def selected_model_Fn(message , history) :
    if model_selected[0] == "GPT" :
         stream = chat_fn_chatgpt(message, history)
         response = ""
         for chunk in stream:
            response += chunk.choices[0].delta.content or ''
            yield response
    elif model_selected[0] == "Claude" : 
        result = chat_fn_claude(message, history)
        response = ""
        with result as stream:
            for text in stream.text_stream:
                response += text or ''
                yield response

def upload_file(files) : 
    # Handle files if file_count = "single"
    if(type(files) != list) : 
        summarize_content_pdf(files)
        return files
    # Handle files if file_count = "multiple"
    else :
      file_paths = [file.name for file in files]
      summarize_content_pdf(file_paths[0])
      return file_paths
    
with gr.Blocks() as demo : 
    with gr.Row() : 
        gr.Markdown("## RexAI : Summarize and Analyze Resumes with AI")
    with gr.Row() :
        with gr.Column() : 
            # Uploading the file using gradio UploadButton component.
            file_upload = gr.File()
            upload_button = gr.UploadButton(label="Click to Upload a File", file_types=['.pdf'], file_count="single")
            upload_button.upload(upload_file, upload_button, file_upload);

            # Creating a dropdown to select the model.
            dropDown = gr.Dropdown(choices=["GPT", "Claude"], label="Select model", inputs=["GPT", "Claude"]);
            dropDown.change(model_chosen, dropDown);
        with gr.Column() : 
            chat_input = gr.ChatInterface(fn=selected_model_Fn, type="messages");


if __name__ == "__main__":
   demo.launch(server_name='0.0.0.0',server_port=port)