class Answer:
    def __init__(self, content: str, latency: int = 0, tokens_prompt: int = 0, tokens_completion: int = 0, retrieval_context: dict = None):
        self.content = content
        self.latency = latency
        self.tokens_prompt = tokens_prompt
        self.tokens_completion = tokens_completion
        self.retrieval_context = retrieval_context
