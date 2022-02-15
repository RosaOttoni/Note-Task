# ***System Modeling***

##

### **Requisitos**

 1- Baixar uma IDE associada ao Python. Aconselha- se baixar o Pycharm. 
        
            As recomendações estão em um arquivo.pdf "Run_code <pt-br>
----------
### **Criação de um ambiente virtual (não é necessário caso esteja fazendo um clone deste terminal)**

Prompt do Anaconda:

- Crie um ambiente utilizando o conda

```
      conda create -n system_modeling_env python=3.9
```

- Ativar o ambiente

```
      conda activate system_modeling_env
```

- Instalando dependencias

```commandline
    pip install -r requirements.txt
```

--------

### **Modelagem de sistemas através da criação de um site** 

O projeto será construido através de dois métodos:

      1- Front end: Bootstrap (HTML + CSS + JavaScript)
      2- Back end: Flask (Python)

O intuito será realizar uma integração com o banco de dados, na qual os usuários poderão se cadastrar e realizar login no site. 

---------

### Comandos necessários para a visualização do banco de dados. 

**No Python Console**

                  from general_system import data_base
                  from general_system.models import Ususario
                  
                  Usuario.query.all() #Verificar os usuários que estão na base de dados. 
                
                  # Quando desejar buscar um usuário específico.
                  usuario = Usuario.query.filter_by(email='nome_do_email_de_cadastro').first()
                  usuario.email
                  usuario.password
                  usuario.username
                  # Quando desejar buscar um usuário específio pelo id (primmary_key).
                  usuario - Usuario.query.get(int('id'))
                  
