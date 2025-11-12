import os
from dotenv import load_dotenv
import gradio as gr
from modules.process_pdf import pdf_processor
from modules.qa_chain import create_qa_chain

load_dotenv()

def process_pdf_and_create_chain(pdf_file):
    """Process the uploaded PDF and create a QA chain."""
    if not pdf_file:
        return None, "⚠️ Please upload a PDF file first."
    try:
        documents = pdf_processor(pdf_file.name)
        combined_text = "\n\n".join([doc.page_content for doc in documents])
        qa_chain = create_qa_chain(combined_text)
        return qa_chain, "✅ PDF processed and QA chain created successfully."
    except Exception as e:
        return None, f"❌ Error processing PDF: {str(e)}"

def chat_with_pdf(message, history, chain):
    """Handle conversation with the PDF."""
    if not chain:
        return history + [[message, "⚠️ Please upload and process a PDF first."]]
    try:
        response = chain.invoke(message)
        history.append([message, response])
        return history
    except Exception as e:
        history.append([message, f"❌ Error: {e}"])
        return history

# Gradio UI
with gr.Blocks(theme=gr.themes.Soft(primary_hue="indigo", secondary_hue="blue")) as demo:
    gr.Markdown(
        """
        # 📄 Doxa - PDF RAG Chatbot  
        Upload a PDF and **chat with it in real time** 💬  
        """
    )

    state = gr.State()
    
    pdf_input = gr.File(label="Upload your PDF", file_types=[".pdf"])
    status = gr.Markdown("Waiting for a PDF upload...")
    process_btn = gr.Button("Process PDF", variant="primary")
    chatbot = gr.Chatbot(height=400, show_copy_button=True)
    msg = gr.Textbox(placeholder="Ask a question about your PDF...", label="Chat")

    process_btn.click(process_pdf_and_create_chain, inputs=[pdf_input], outputs=[state, status])
    msg.submit(chat_with_pdf, inputs=[msg, chatbot, state], outputs=[chatbot])


if __name__ == "__main__":
    demo.launch(share=True)