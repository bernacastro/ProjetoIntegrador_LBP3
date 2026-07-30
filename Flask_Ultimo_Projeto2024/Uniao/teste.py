def antiXSS(valor):
        for char in valor:
            if char == "<" or char ==">" or char == "'" or char == "=" or char == '"':
                print("Erro: tentativa de XSS")
                return True
                

def verificarSenha(self, senha):
        try:
            if len(senha) < 8:
                return "A senha deve ter mais de 8 caracteres."
            maiuscula = False
            minuscula = False
            especial = False
            for char in senha:
                if char.isupper():
                    maiuscula = True
                elif char.islower():
                    minuscula = True
                elif char in "!@#$%^&*()-=+[]{}|;:,.<>?/~":
                    especial = True

            if not maiuscula:
                return "A senha deve conter pelo menos uma letra maiúscula."
            if not minuscula:
                return "A senha deve conter pelo menos uma letra minúscula."
            if not especial:
                return "A senha deve conter pelo menos um caractere especial."

            return True
        except Exception as e:
            print(f"Erro ao verificar a senha: {e}")
            return None

