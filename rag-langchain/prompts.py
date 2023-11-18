from langchain.prompts.prompt import PromptTemplate
from langchain.prompts import ChatPromptTemplate

standalone_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language.
                      Chat History:
                      {chat_history}
                      Follow Up Input: {question}
                      Standalone question:
                      """
STANDALONE_QUESTION_PROMPT = PromptTemplate.from_template(standalone_template)

answer_template = """Answer the question based only on the following context:
                    {context}

                    Question: {question}
                  """
ANSWER_PROMPT = ChatPromptTemplate.from_template(answer_template)
DEFAULT_DOCUMENT_PROMPT = PromptTemplate.from_template(template="{page_content}")
