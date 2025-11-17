# 🔗 Guia de Integração: Notebooks → Django → React

## 🎯 Problema Atual

Você tem:
- ✅ Notebooks Jupyter com análises funcionando (13.ipynb e 15.ipynb)
- ✅ Frontend React esperando dados
- ❌ Nenhuma conexão entre eles

## 📦 O que o Backend Django Precisa Fazer

### Transformar análises em **APIs REST** que retornem **JSON**

**Exemplo de fluxo:**
```
Frontend React → GET /api/energia/analise → Django Backend → Processa CSV → Retorna JSON → React exibe
```

---

## 🔄 Estratégia de Integração

### Opção 1: **Reutilizar Lógica dos Notebooks** ⭐ (Recomendado)

Você vai:
1. Criar **funções Python** com a lógica dos notebooks
2. Chamar essas funções nas **Views do Django**
3. Retornar os resultados como **JSON**

### Opção 2: **Gerar Imagens e Retornar URLs**

Você vai:
1. Gerar gráficos como arquivos de imagem
2. Salvar em `/static` ou `/media`
3. Retornar URLs das imagens

**Vou focar na Opção 1 (mais moderna e flexível)**

---

## 📋 Exemplo Prático: Painéis Solares

### 1️⃣ **Estrutura de Pastas Recomendada**

```
backend/
├── energyAPI/
│   ├── models.py           # (opcional, se quiser salvar no DB)
│   ├── views.py            # Endpoints da API
│   ├── serializers.py      # Formatação JSON
│   ├── urls.py             # Rotas da API
│   └── services/           # ⭐ NOVA PASTA
│       └── analise_energia.py  # Lógica do notebook aqui
└── heartAPI/
    └── services/
        └── analise_saude.py
```

### 2️⃣ **Extrair Lógica do Notebook para Função**

**Arquivo: `energyAPI/services/analise_energia.py`**

```python
import pandas as pd
import numpy as np
from pathlib import Path

# Caminho base para os dados
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_PATH = BASE_DIR / 'dados' / 'painel_solar.csv'

def calcular_rendimento():
    """
    Calcula o rendimento dos painéis solares.
    
    Returns:
        dict: Dados processados prontos para JSON
    """
    # Carregar dados
    df = pd.read_csv(DATA_PATH)
    
    # Calcular rendimento (mesma lógica do notebook)
    area_painel = 10
    df['potencia_incidente_kw'] = (df['radiacao_wm2'] * area_painel) / 1000
    df['rendimento_percent'] = (df['potencia_kw'] / df['potencia_incidente_kw']) * 100
    
    # Preparar dados para retornar
    resultado = {
        'dados_brutos': df.to_dict('records'),  # Lista de dicionários
        'rendimento_por_hora': df.groupby('hora')['rendimento_percent'].mean().to_dict(),
        'estatisticas': {
            'rendimento_medio': round(df['rendimento_percent'].mean(), 2),
            'rendimento_maximo': round(df['rendimento_percent'].max(), 2),
            'hora_pico': int(df.loc[df['rendimento_percent'].idxmax(), 'hora']),
            'potencia_maxima': round(df['potencia_kw'].max(), 1),
        },
        'dados_grafico_dispersao': {
            'temperatura': df['temperatura_c'].tolist(),
            'potencia': df['potencia_kw'].tolist(),
        }
    }
    
    return resultado


def calcular_correlacao():
    """
    Calcula correlações entre variáveis.
    
    Returns:
        dict: Matriz de correlação e insights
    """
    df = pd.read_csv(DATA_PATH)
    
    # Calcular correlação
    correlacao = df[['temperatura_c', 'radiacao_wm2', 'potencia_kw']].corr()
    
    return {
        'matriz_correlacao': correlacao.to_dict(),
        'correlacao_temp_potencia': round(correlacao.loc['temperatura_c', 'potencia_kw'], 3)
    }
```

**⚠️ Pontos Importantes:**
- Função retorna **dicionários Python** (facilmente convertidos para JSON)
- Usa `to_dict()` e `tolist()` para converter Pandas em tipos nativos
- Agrupa lógica relacionada em funções separadas
- Paths relativos usando `Path`

---

### 3️⃣ **Criar View no Django REST Framework**

**Arquivo: `energyAPI/views.py`**

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .services.analise_energia import calcular_rendimento, calcular_correlacao

@api_view(['GET'])
def analise_rendimento(request):
    """
    Endpoint: GET /api/energia/rendimento
    
    Retorna análise completa de rendimento dos painéis solares.
    """
    try:
        dados = calcular_rendimento()
        return Response(dados, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'erro': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def correlacao_variaveis(request):
    """
    Endpoint: GET /api/energia/correlacao
    """
    try:
        dados = calcular_correlacao()
        return Response(dados, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'erro': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
```

**⚠️ O que acontece aqui:**
- `@api_view(['GET'])` → define que é um endpoint GET
- `Response()` → retorna JSON automaticamente
- Try/except → captura erros e retorna mensagem amigável

---

### 4️⃣ **Configurar Rotas**

**Arquivo: `energyAPI/urls.py`** (CRIAR ESTE ARQUIVO)

```python
from django.urls import path
from . import views

urlpatterns = [
    path('rendimento/', views.analise_rendimento, name='analise_rendimento'),
    path('correlacao/', views.correlacao_variaveis, name='correlacao_variaveis'),
]
```

**Arquivo: `backend/urls.py`** (MODIFICAR)

```python
from django.contrib import admin
from django.urls import path, include  # ← adicionar include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/energia/', include('energyAPI.urls')),  # ← ADICIONAR
    path('api/saude/', include('heartAPI.urls')),     # ← ADICIONAR
]
```

---

### 5️⃣ **Configurar CORS (para o React acessar)**

**Arquivo: `backend/settings.py`**

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',        # ← ADICIONAR
    'corsheaders',           # ← ADICIONAR
    
    # Seus apps
    'energyAPI',             # ← ADICIONAR
    'heartAPI',              # ← ADICIONAR
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # ← ADICIONAR (antes do CommonMiddleware)
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuração CORS (permitir React acessar)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Vite dev server
    "http://127.0.0.1:5173",
]

# Configuração do Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}
```

---

## 🌐 Como o Frontend React Vai Consumir

### No componente `Energia.jsx`:

```jsx
import React, { useEffect, useState } from "react";

export default function Energia() {
  const [dados, setDados] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Chamar API do Django
    fetch('http://localhost:8000/api/energia/rendimento/')
      .then(response => response.json())
      .then(data => {
        setDados(data);
        setLoading(false);
      })
      .catch(error => console.error('Erro:', error));
  }, []);

  if (loading) return <div>Carregando...</div>;

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6">Análise de Energia Solar</h1>
      
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-white p-4 rounded shadow">
          <h2 className="text-xl font-semibold">Estatísticas</h2>
          <p>Rendimento Médio: {dados.estatisticas.rendimento_medio}%</p>
          <p>Hora Pico: {dados.estatisticas.hora_pico}h</p>
          <p>Potência Máxima: {dados.estatisticas.potencia_maxima} kW</p>
        </div>
        
        <div className="bg-white p-4 rounded shadow">
          <h2 className="text-xl font-semibold">Dados Brutos</h2>
          <ul>
            {dados.dados_brutos.map((item, index) => (
              <li key={index}>
                {item.hora}h: {item.potencia_kw} kW
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
```

---

## 📊 Exemplo de Resposta JSON

### Quando você chamar `GET http://localhost:8000/api/energia/rendimento/`

```json
{
  "dados_brutos": [
    {
      "hora": 8,
      "temperatura_c": 24,
      "radiacao_wm2": 680,
      "potencia_kw": 3.2,
      "rendimento_percent": 47.06
    },
    {
      "hora": 10,
      "temperatura_c": 28,
      "radiacao_wm2": 850,
      "potencia_kw": 3.9,
      "rendimento_percent": 45.88
    }
  ],
  "rendimento_por_hora": {
    "8": 47.06,
    "10": 45.88,
    "12": 44.57,
    "14": 42.55,
    "16": 41.38
  },
  "estatisticas": {
    "rendimento_medio": 44.29,
    "rendimento_maximo": 47.06,
    "hora_pico": 8,
    "potencia_maxima": 4.1
  },
  "dados_grafico_dispersao": {
    "temperatura": [24, 28, 32, 34, 31],
    "potencia": [3.2, 3.9, 4.1, 4.0, 3.6]
  }
}
```

---

## 🎨 Para Gráficos no Frontend

Você pode usar bibliotecas como:

### **Chart.js** ou **Recharts** (React)

```jsx
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';

<LineChart width={600} height={300} data={dados.dados_brutos}>
  <CartesianGrid strokeDasharray="3 3" />
  <XAxis dataKey="hora" />
  <YAxis />
  <Tooltip />
  <Line type="monotone" dataKey="potencia_kw" stroke="#8884d8" />
</LineChart>
```

---

## 📝 Checklist de Implementação

### Configuração Inicial
- [ ] Criar pasta `services/` em `energyAPI` e `heartAPI`
- [ ] Adicionar `rest_framework` e `corsheaders` no `INSTALLED_APPS`
- [ ] Configurar `CORS_ALLOWED_ORIGINS` no settings
- [ ] Adicionar middleware do CORS

### Energia API
- [ ] Criar `analise_energia.py` com funções
- [ ] Criar views com `@api_view`
- [ ] Criar `energyAPI/urls.py`
- [ ] Incluir no `backend/urls.py`
- [ ] Testar endpoint no navegador

### Saúde API
- [ ] Criar `analise_saude.py` com funções
- [ ] Criar views
- [ ] Criar `heartAPI/urls.py`
- [ ] Incluir no `backend/urls.py`

### Frontend
- [ ] Fazer fetch dos endpoints
- [ ] Exibir dados em componentes React
- [ ] Adicionar gráficos com Chart.js/Recharts

---

## 🔍 Como Testar

### 1. Iniciar Django:
```bash
cd backend
python manage.py runserver
```

### 2. Abrir no navegador:
```
http://localhost:8000/api/energia/rendimento/
```

Você deve ver o JSON!

### 3. Iniciar React:
```bash
cd frontend
npm run dev
```

---

## 💡 Conceitos Importantes

### **Serializers vs Dicionários**

Para projetos simples: **Use dicionários** (como mostrei)
```python
return Response({'dados': [1, 2, 3]})
```

Para projetos complexos: **Use Serializers**
```python
class EnergiaSerializer(serializers.Serializer):
    hora = serializers.IntegerField()
    potencia = serializers.FloatField()
```

### **Quando usar Models vs CSV direto?**

- **CSV direto** → dados não mudam, análises pontuais ✅ (seu caso)
- **Models/DB** → dados inseridos por usuários, precisam ser persistidos

---

## 🚀 Próximos Passos

1. **Implemente a Energia API primeiro** (mais simples)
2. **Teste no navegador** antes de conectar ao React
3. **Depois replique** para a Saúde API
4. **Por último**, conecte o frontend

---

## 📚 Recursos para Estudar

- [Django REST Framework - Quickstart](https://www.django-rest-framework.org/tutorial/quickstart/)
- [Django CORS Headers](https://github.com/adamchainz/django-cors-headers)
- [Pandas to JSON](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_json.html)

---

**Pronto para começar?** Me chame quando tiver dúvidas! 🎉
