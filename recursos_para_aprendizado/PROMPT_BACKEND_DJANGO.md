# Prompt para Desenvolvimento Backend Django - Projeto UBD

## 🎯 Objetivo do Projeto

Estou desenvolvendo um backend Django para uma aplicação full-stack de análise de dados. O objetivo é **aprender Django** através da prática, usando IA como ferramenta de ensino e não como substituta do meu aprendizado.

## 📊 Contexto do Projeto

### Estrutura Atual

```
UBD/
├── backend/                    # Django (em desenvolvimento)
│   ├── manage.py
│   └── backend/
│       ├── settings.py        # Configuração básica já existe
│       ├── urls.py            # Apenas admin configurado
│       └── wsgi.py
├── frontend/                   # React + Vite (já desenvolvido)
│   ├── src/
│   │   └── pages/
│   │       ├── Energia.jsx    # Página para análise solar
│   │       └── Saude.jsx      # Página para análise cardíaca
│   └── ...
└── dados/                      # Datasets CSV
    ├── painel_solar.csv       # hora, temperatura_c, radiacao_wm2, potencia_kw
    └── risco_cardiaco.csv     # paciente, idade, colesterol, pressao, risco
```

### Stack Tecnológica Instalada

- **Django 5.2.8** - Framework web
- **Django REST Framework 3.16.1** - Para criar APIs
- **Django CORS Headers 4.9.0** - Para permitir requisições do frontend
- **djangorestframework-simplejwt 5.5.1** - Para autenticação JWT (se necessário)
- **psycopg2-binary 2.9.11** - Driver PostgreSQL
- **python-dotenv 1.2.1** - Variáveis de ambiente
- **pandas, matplotlib, seaborn, scikit-learn** - Análise de dados

### Funcionalidades Desejadas

#### 1. Análise de Painéis Solares (Minimundo 13)
- **Dataset**: `painel_solar.csv`
- **Campos**: hora, temperatura_c, radiacao_wm2, potencia_kw
- **Análises**:
  - Cálculo de rendimento médio por hora
  - Gráfico de dispersão (temperatura × potência)
  - Mapa de calor (hora × eficiência)

#### 2. Análise de Risco Cardíaco (Minimundo 15)
- **Dataset**: `risco_cardiaco.csv`
- **Campos**: paciente, idade, colesterol, pressao, risco
- **Análises**:
  - Análise de correlação entre variáveis
  - Visualizações de dispersão
  - Mapas de calor de correlação
  - Predição de risco (ML opcional)

## 🎓 Minha Abordagem de Aprendizado

### O que eu QUERO aprender:

1. **Arquitetura Django**:
   - Estrutura de apps Django
   - Models, Views, Serializers
   - URLs e roteamento
   - Boas práticas de organização

2. **Django REST Framework**:
   - Criação de APIs RESTful
   - Serializers e validação
   - ViewSets vs APIViews
   - Autenticação e permissões

3. **Integração de Dados**:
   - Como trabalhar com CSV no Django
   - Processar e analisar dados em views
   - Retornar dados processados via API
   - Cachear resultados quando apropriado

4. **CORS e Comunicação Frontend**:
   - Configurar CORS corretamente
   - Estruturar respostas JSON
   - Tratamento de erros

### Como eu quero que você me ajude:

✅ **FAÇA**:
- Explique os conceitos antes de mostrar código
- Mostre exemplos práticos e didáticos
- Aponte boas práticas e por que são importantes
- Explique cada linha de código importante
- Sugira recursos para eu estudar mais
- Me faça perguntas para verificar meu entendimento
- Mostre alternativas e trade-offs

❌ **NÃO FAÇA**:
- Gerar código completo sem explicação
- Assumir que eu sei conceitos avançados
- Pular etapas de configuração
- Usar "magia" sem explicar
- Implementar tudo de uma vez

## 🚀 Tarefas de Desenvolvimento

### Fase 1: Estrutura Básica
- [ ] Criar app Django para análises (`analytics` ou similar)
- [ ] Configurar CORS para o frontend React
- [ ] Estruturar models (se necessário para o projeto)
- [ ] Configurar rotas básicas da API

### Fase 2: Análise de Painéis Solares
- [ ] Endpoint para carregar dados do CSV
- [ ] Endpoint para cálculos de rendimento
- [ ] Endpoint para dados de gráficos
- [ ] Serializers apropriados

### Fase 3: Análise de Risco Cardíaco
- [ ] Endpoint para carregar dados de saúde
- [ ] Endpoint para análise de correlação
- [ ] Endpoint para dados de visualização
- [ ] (Opcional) Endpoint para predição ML

### Fase 4: Otimizações
- [ ] Cache de análises
- [ ] Tratamento de erros robusto
- [ ] Documentação da API
- [ ] Testes básicos

## 📝 Formato de Resposta Ideal

Quando eu pedir ajuda, estruture assim:

### 1. Conceito
> Explique o conceito/padrão que será usado

### 2. Implementação Passo a Passo
> Mostre o código com explicações linha a linha

### 3. Pontos de Atenção
> Erros comuns, gotchas, boas práticas

### 4. Próximos Passos
> O que aprender/fazer em seguida

### 5. Recursos de Estudo
> Links para documentação oficial, tutoriais, etc.

## ❓ Exemplo de Pergunta que Farei

"Preciso criar um endpoint que carregue os dados de `painel_solar.csv`, calcule o rendimento médio por hora e retorne em formato JSON. Como fazer isso seguindo as boas práticas do Django REST Framework? Explique cada parte do código."

## 🔧 Configuração Atual

**Django Settings Relevantes**:
```python
# settings.py já configurado com:
- Django 5.2.8
- SECRET_KEY (desenvolvimento)
- DEBUG = True
- SQLite database
- Instalações: django-cors-headers, rest_framework, etc.
```

**URLs Atuais**:
```python
# urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    # Preciso adicionar rotas da API aqui
]
```

## 🎯 Meu Nível de Conhecimento

- ✅ Conheço Python básico/intermediário
- ✅ Entendo conceitos de API REST
- ✅ Já trabalhei com React/Frontend
- ⚠️ Django é novo para mim
- ⚠️ Preciso aprender sobre Models, Views, Serializers
- ⚠️ Primeira vez usando Django REST Framework

## 🤝 Expectativa

Quero que me ajude a construir este backend de forma **educativa**, onde eu entenda cada decisão de arquitetura, cada linha de código importante, e me torne capaz de desenvolver sozinho projetos Django no futuro.

---

**Nota**: Este projeto é acadêmico e focado em aprendizado. Priorize explicações claras e código didático sobre otimizações avançadas.
