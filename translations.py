import re
import pypinyin

# 翻译字典
translations = {
    'zh': {
        # 通用
        'app_name': '城市新闻情感分析系统',
        'navbar_brand': '城市情感分析',
        'home': '首页',
        'city_list': '城市列表',
        'upload_data': '上传数据',
        'search': '搜索',
        'search_city': '搜索城市...',
        'profile': '个人中心',
        'logout': '退出登录',
        'login': '登录',
        'register': '注册',
        
        # 首页
        'app_description': '通过分析新闻媒体报道，深入了解各城市的公众形象和情感倾向，为城市发展和决策提供数据支持。',
        'analyzed_cities': '分析城市数量',
        'news_data_amount': '新闻数据量',
        'real_time_analysis': '实时',
        'as_of_date': '截止至2025.5.28',
        'data_analysis': '数据分析',
        'top_cities': '情感得分最高的城市',
        'bottom_cities': '情感得分最低的城市',
        'view_all': '查看全部',
        'rank': '排名',
        'city': '城市',
        'sentiment_score': '情感分数',
        'news_count': '新闻数量',
        'actions': '操作',
        'details': '详情',
        'no_data': '暂无数据',
        'upload_prompt': '想要上传自己的城市新闻数据进行分析？',
        'register_to_upload': '注册账户后，您可以上传自定义的新闻数据，获取城市情感分析报告。',
        'upload_news': '上传新闻数据进行分析',
        
        # 城市列表
        'all_cities_ranking': '全部城市情感排名',
        'total_cities': '共 {0} 个城市',
        'positive_ratio': '积极情感占比',
        'neutral_ratio': '中性情感占比',
        'negative_ratio': '消极情感占比',
        'positive_pct': '正面比例',
        'negative_pct': '负面比例',
        
        # 城市详情
        'sentiment_analysis_details': '情感分析详情',
        'ranking_situation': '排名情况',
        'national_ranking': '全国排名',
        'better_than': '超过全国 {0}% 的城市',
        'statistics': '数据统计',
        'positive_news_ratio': '正面新闻比例',
        'negative_news_ratio': '负面新闻比例',
        'neutral_news_ratio': '中性新闻比例',
        'positive': '正面',
        'neutral': '中性',
        'negative': '负面',
        'sentiment_distribution': '情感分布',
        'positive_news': '正面新闻',
        'neutral_news': '中性新闻',
        'negative_news': '负面新闻',
        'analysis_conclusion': '分析结论',
        'analysis_summary': '基于对{0}的{1}条新闻的情感分析，该城市的整体情感分数为{2}，在全国排名第{3}位。',
        'very_positive': '该城市的新闻情感整体非常积极，正面新闻占比达到{0}%，远高于负面新闻。这表明该城市的公共形象和新闻报道整体呈现出非常积极的态势。',
        'positive_sentiment': '该城市的新闻情感整体较为积极，正面新闻占比为{0}%，高于负面新闻。这表明该城市的公共形象和新闻报道整体呈现出积极的态势。',
        'neutral_sentiment': '该城市的新闻情感整体中性偏积极，正面新闻占比为{0}%，负面新闻占比为{1}%。这表明该城市的公共形象和新闻报道呈现出较为平衡的态势。',
        'negative_sentiment': '该城市的新闻情感整体偏负面，负面新闻占比达到{0}%，高于正面新闻。这表明该城市的公共形象和新闻报道整体呈现出较为负面的态势。',
        'back_to_list': '返回城市列表',
        'upload_city_news': '上传{0}的新闻数据进行分析',
        'login_to_upload': '登录后上传数据',
        
        # 登录/注册
        'username': '用户名',
        'password': '密码',
        'confirm_password': '确认密码',
        'register_success': '注册成功，请登录',
        'username_exists': '已有账号？',
        'invalid_credentials': '用户名或密码错误',
        'empty_fields': '用户名和密码不能为空',
        'password_mismatch': '两次输入的密码不一致',
        
        # 上传
        'upload_title': '上传新闻数据',
        'city_name': '城市名称',
        'select_file': '选择文件',
        'upload': '上传',
        'file_note': '注意：仅支持CSV格式文件，且必须包含"title"或"content"列',
        'upload_success': '文件上传成功并完成分析: {0}',
        'no_file': '没有选择文件',
        'empty_fields_upload': '文件名或城市名不能为空',
        'csv_only': '只支持CSV文件',
        'missing_columns': 'CSV文件缺少必要的列：title或content',
        'no_news': '没有找到有效的新闻内容',
        'analysis_error': '分析出错: {0}',
        
        # 页脚
        'about': '关于',
        'quick_links': '快速链接',
        'copyright': '© 2025 城市新闻情感分析系统',
        'powered_by': '使用BERT模型进行情感分析',
        'app_description_footer': '基于深度学习的城市新闻情感分析工具，帮助了解城市的媒体形象和公众情感。'
    },
    'es': {
        # General
        'app_name': 'Sistema de Análisis de Sentimiento de Noticias de Ciudades',
        'navbar_brand': 'Análisis de Sentimiento',
        'home': 'Inicio',
        'city_list': 'Lista de Ciudades',
        'upload_data': 'Subir Datos',
        'search': 'Buscar',
        'search_city': 'Buscar ciudad...',
        'profile': 'Centro Personal',
        'logout': 'Cerrar Sesión',
        'login': 'Iniciar Sesión',
        'register': 'Registrarse',
        
        # Home page
        'app_description': 'A través del análisis de informes de medios de noticias, comprenda profundamente la imagen pública y las tendencias emocionales de varias ciudades, proporcionando apoyo de datos para el desarrollo y la toma de decisiones de la ciudad.',
        'analyzed_cities': 'Ciudades Analizadas',
        'news_data_amount': 'Cantidad de Datos',
        'real_time_analysis': 'Tiempo Real',
        'as_of_date': 'Hasta 28/5/2025',
        'data_analysis': 'Análisis de Datos',
        'top_cities': 'Ciudades con Mayor Puntuación de Sentimiento',
        'bottom_cities': 'Ciudades con Menor Puntuación de Sentimiento',
        'view_all': 'Ver Todo',
        'rank': 'Rango',
        'city': 'Ciudad',
        'sentiment_score': 'Puntuación',
        'news_count': 'Cantidad',
        'actions': 'Acciones',
        'details': 'Detalles',
        'no_data': 'Sin Datos',
        'upload_prompt': '¿Quieres subir tus propios datos de noticias de la ciudad para análisis?',
        'register_to_upload': 'Después de registrarte, puedes subir datos de noticias personalizados y obtener un informe de análisis de sentimiento de la ciudad.',
        'upload_news': 'Subir Datos de Noticias para Análisis',
        
        # City list
        'all_cities_ranking': 'Clasificación de Sentimiento de Todas las Ciudades',
        'total_cities': 'Total {0} Ciudades',
        'positive_ratio': 'Ratio Positivo',
        'neutral_ratio': 'Ratio Neutral',
        'negative_ratio': 'Ratio Negativo',
        'positive_pct': 'Positivo',
        'negative_pct': 'Negativo',
        
        # City detail
        'sentiment_analysis_details': 'Detalles del Análisis de Sentimiento',
        'ranking_situation': 'Situación de Ranking',
        'national_ranking': 'Ranking Nacional',
        'better_than': 'Supera al {0}% de las ciudades del país',
        'statistics': 'Estadísticas',
        'positive_news_ratio': 'Ratio de Noticias Positivas',
        'negative_news_ratio': 'Ratio de Noticias Negativas',
        'neutral_news_ratio': 'Ratio de Noticias Neutrales',
        'positive': 'Positivo',
        'neutral': 'Neutral',
        'negative': 'Negativo',
        'sentiment_distribution': 'Distribución de Sentimiento',
        'positive_news': 'Noticias Positivas',
        'neutral_news': 'Noticias Neutrales',
        'negative_news': 'Noticias Negativas',
        'analysis_conclusion': 'Conclusión del Análisis',
        'analysis_summary': 'Basado en el análisis de sentimiento de {1} noticias de {0}, la puntuación general de sentimiento de esta ciudad es {2}, clasificada en el puesto {3} a nivel nacional.',
        'very_positive': 'El sentimiento general de las noticias de esta ciudad es muy positivo, con un porcentaje de noticias positivas de {0}%, mucho más alto que las noticias negativas. Esto indica que la imagen pública y los informes de noticias de esta ciudad presentan una tendencia muy positiva.',
        'positive_sentiment': 'El sentimiento general de las noticias de esta ciudad es relativamente positivo, con un porcentaje de noticias positivas de {0}%, mayor que las noticias negativas. Esto indica que la imagen pública y los informes de noticias de esta ciudad presentan una tendencia positiva.',
        'neutral_sentiment': 'El sentimiento general de las noticias de esta ciudad es neutral con tendencia positiva, con un porcentaje de noticias positivas de {0}% y un porcentaje de noticias negativas de {1}%. Esto indica que la imagen pública y los informes de noticias de esta ciudad presentan una tendencia relativamente equilibrada.',
        'negative_sentiment': 'El sentimiento general de las noticias de esta ciudad es relativamente negativo, con un porcentaje de noticias negativas de {0}%, mayor que las noticias positivas. Esto indica que la imagen pública y los informes de noticias de esta ciudad presentan una tendencia relativamente negativa.',
        'back_to_list': 'Volver a la Lista',
        'upload_city_news': 'Subir Datos de Noticias de {0} para Análisis',
        'login_to_upload': 'Iniciar Sesión para Subir',
        
        # Login/Register
        'username': 'Nombre de Usuario',
        'password': 'Contraseña',
        'confirm_password': 'Confirmar Contraseña',
        'register_success': 'Registro exitoso, por favor inicia sesión',
        'username_exists': '¿Ya tienes una cuenta?',
        'invalid_credentials': 'Nombre de usuario o contraseña incorrectos',
        'empty_fields': 'El nombre de usuario y la contraseña no pueden estar vacíos',
        'password_mismatch': 'Las contraseñas no coinciden',
        
        # Upload
        'upload_title': 'Subir Datos de Noticias',
        'city_name': 'Nombre de la Ciudad',
        'select_file': 'Seleccionar Archivo',
        'upload': 'Subir',
        'file_note': 'Nota: Solo se admiten archivos CSV y deben incluir columnas "title" o "content"',
        'upload_success': 'Archivo subido con éxito y análisis completo: {0}',
        'no_file': 'No se seleccionó ningún archivo',
        'empty_fields_upload': 'El nombre del archivo o de la ciudad no puede estar vacío',
        'csv_only': 'Solo se admiten archivos CSV',
        'missing_columns': 'El archivo CSV carece de las columnas necesarias: title o content',
        'no_news': 'No se encontró contenido de noticias válido',
        'analysis_error': 'Error de análisis: {0}',
        
        # Footer
        'about': 'Acerca de',
        'quick_links': 'Enlaces Rápidos',
        'copyright': '© 2025 Sistema de Análisis de Sentimiento de Noticias de Ciudades',
        'powered_by': 'Impulsado por el modelo BERT para análisis de sentimiento',
        'app_description_footer': 'Herramienta de análisis de sentimiento de noticias de ciudades basada en aprendizaje profundo, ayudando a comprender la imagen mediática y el sentimiento público de las ciudades.'
    }
}

# 城市名称汉字到拼音的转换
def chinese_to_pinyin(chinese_name):
    """将中文城市名转换为拼音"""
    # 如果已经是拼音（只包含字母、数字和空格），则直接返回
    if re.match(r'^[a-zA-Z0-9\s]+$', chinese_name):
        return chinese_name
    
    # 转换为拼音，并首字母大写
    pinyin_list = pypinyin.pinyin(chinese_name, style=pypinyin.NORMAL)
    pinyin_name = ''.join([p[0] for p in pinyin_list])
    return pinyin_name.capitalize()

# 城市名拼音对照表
city_name_mapping = {}

def get_city_name(city, lang='zh'):
    """根据语言获取城市名称"""
    if lang == 'zh':
        return city
    else:
        if city not in city_name_mapping:
            city_name_mapping[city] = chinese_to_pinyin(city)
        return city_name_mapping[city]

def get_text(key, lang='zh', *args):
    """获取指定语言的文本，支持格式化参数"""
    if key not in translations[lang]:
        # 如果找不到翻译，返回中文版本
        text = translations['zh'].get(key, key)
    else:
        text = translations[lang][key]
    
    # 如果提供了参数，进行格式化
    if args:
        try:
            return text.format(*args)
        except:
            return text
    return text 