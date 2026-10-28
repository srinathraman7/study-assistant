import os
from google import genai
from google.genai import types
client = genai.Client(api_key = os.getenv('GEMINI_API_KEY'))
import gradio as gr

personalities = {
  "Friendly":
  """You are a friendly, enthusiastic, and highly encouraging Study Assistant.
  Your goal is to break down complex concepts into simple, beginner-friendly explanations.
  Use analogies and real-world examples that beginners can relate to.
  Always ask a follow-up question to check understanding""",
  "Academic":
  """You are a strictly academic, highly detailed, and professional university Professor.
  Use precise, formal terminology, cite key concepts and structure your response.
  Your goal is to break down complex concepts into simple, beginner-friendly explanations.
  Use analogies and real-world examples that beginners can relate to.
  Always ask a follow-up question to check understanding"""
}

def study_assisstent(user_prompt, persona):

  response = client.models.generate_content(
      model = "gemini-3.5-flash-lite",
      config = types.GenerateContentConfig(system_instruction= personalities[persona],
                                           temperature=0.3,
                                           ),
      contents = user_prompt
  )
  return response.text

demo= gr.Interface(
    fn=study_assisstent,
    inputs=[
        gr.Textbox(lines=3, placeholder="ask what you want...", label="Question"),
        gr.Radio(choices=list(personalities.keys()), value="Friendly", label="Personality")
    ],
    outputs=gr.Textbox(lines=4, label="Response"),
    title="Study Assistent Guide",
    description="Ask a question and get an answer from your AI study assistant with a chosen personality."
)

demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
