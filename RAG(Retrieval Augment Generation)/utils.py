class MistralPrompts:
    
    # Create a standalone question prompt by using chat history and followup question.
    @staticmethod
    def create_standalone_question_prompt(question, chat_history_prompt):
        message = f'''
                [INST]
                Taking chat history as context, rephrase follow up question into a standalone question.
                "Follow up question: {question}
                [/INST]
              '''
        prompt = chat_history_prompt + message
        return prompt

    # Create a chat history prompt by combining user and bot messages.
    @staticmethod
    def create_history_prompt(chat_history):
        user_message, bot_message = chat_history[0]
        chat_history_text = f"<s>[INST] {user_message} [/INST] {bot_message}</s>"
        chat_history_text += "".join(f"[INST] {user_message} [/INST] {bot_message}</s>" for user_message, bot_message in chat_history[1:])
        return chat_history_text

    # Create a question prompt by adding context and question to a chat history prompt.
    @staticmethod
    def create_question_prompt(question, context, chat_history_prompt):
        message = '''
              [INST]
              {instructions}
              Context: {context}
              Question: {question}
              [/INST]
              '''
        if chat_history_prompt == '':
            # If no chat history, provide instructions.
            instructions = '''
                          Use the following pieces of information to answer the user's question.
                          If you don't know the answer, just say that you don't know,
                          don't try to make up an answer.
                          '''
            message = message.format(instructions=instructions, context=context, question=question)
            prompt = message
        else:
            # If there's a chat history, add context and question to it.
            message = message.format(instructions='', context=context, question=question)
            prompt = chat_history_prompt + message
        return prompt

    # Extract the response from a prompt.
    @staticmethod
    def extract_response(response):
        response = response.split('[/INST]')[-1].split('</s>')[0].strip()
        return response
