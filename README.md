# Sistema de Análisis de Sentimiento de Noticias Urbanas de China

## Estructura de directorios

```
CityNewsApp/
├── city_news_app.py # Aplicación principal
├── city_news.db # Base de datos SQLite
├── run_app.bat # Archivo por lotes para iniciar la aplicación
├── static/ # Archivo de recursos estáticos
│ ├── css/ # Archivo de estilos CSS
│ └── js/ # Archivo JavaScript
├── templates/ # Archivo de plantilla HTML
├── uploads/ # Directorio de archivos subidos por el usuario
├── jieguo/ # Datos de resultados del análisis
└── news_sentiment_model/ # Modelo de análisis de sentimiento BERT
```

## Guía de instalación

1. Asegúrese de tener instalado Python 3.8 o superior.
2. Instale las bibliotecas de Python necesarias:
```
pip install flask flask-login werkzeug pandas torch transformers
```
3. Asegúrese de que el archivo del modelo BERT esté correctamente ubicado en el directorio `news_sentiment_model`

## Cómo usar

1. Haga doble clic en el archivo por lotes `run_app.bat` para iniciar la aplicación.
2. Visite `http://localhost:5000` en el navegador.
3. Registre una cuenta e inicie sesión en el sistema.
4. Explore los resultados del análisis de sentimiento de la ciudad o cargue datos de noticias para su análisis.


# 中国城市新闻情感分析系统

## 目录结构

```
CityNewsApp/
├── city_news_app.py        # 主应用程序
├── city_news.db            # SQLite数据库
├── run_app.bat             # 启动应用的批处理文件
├── static/                 # 静态资源文件
│   ├── css/                # CSS样式文件
│   └── js/                 # JavaScript文件
├── templates/              # HTML模板文件
├── uploads/                # 用户上传文件目录
├── jieguo/                 # 分析结果数据
└── news_sentiment_model/   # BERT情感分析模型
```

## 安装指南

1. 确保已安装Python 3.8或以上版本
2. 安装必要的Python库：
   ```
   pip install flask flask-login werkzeug pandas torch transformers
   ```
3. 确保BERT模型文件已正确放置在`news_sentiment_model`目录中

## 使用方法

1. 双击运行`run_app.bat`批处理文件启动应用
2. 在浏览器中访问`http://localhost:5000`
3. 注册账户并登录系统
4. 浏览城市情感分析结果或上传新闻数据进行分析
