pipeline {
    agent { label 'docker-vm' }

    environment {
        DOQA_URL = "https://o7g195.doqa.app"
        DOQA_SPACE_ID = "2"
        DOQA_TOKEN = credentials('DOQA_TOKEN')
    }

    stages {
        stage('Checkout SCM') {
            steps { checkout scm }
        }

        stage('Clean Workspace') {
            steps {
                sh '''
                    echo "🧹 Очищаем воркспейс..."
                    rm -rf .pytest_cache allure-results doqa-results *.zip
                    echo "✅ Очистка завершена"
                '''
            }
        }

        stage('Run Playwright Tests') {
            steps {
                sh '''
                    echo "🚀 Запускаем тесты..."
                    docker run --rm --network host -u $(id -u):$(id -g) \
                        -v ${WORKSPACE}:/app \
                        my-playwright:latest \
                        pytest . --cache-clear -v --maxfail=5
                '''
            }
        }
    }

    post {
        always {
            sh '''
                # Проверяем наличие результатов от плагина doqa-pytest
                if [ -d "doqa-results" ] && [ "$(ls -A doqa-results/*-result.json 2>/dev/null)" ]; then
                    echo " Собираем результаты для отправки..."

                    # Создаем Python-скрипт для сборки JSON и отправки на правильный эндпоинт
                    cat > send_to_doqa.py << 'PYEOF'
import json
import glob
import os
import sys
from pathlib import Path

results_dir = "doqa-results"
token = os.environ.get("DOQA_TOKEN", "")
space_id = int(os.environ.get("DOQA_SPACE_ID", "2"))
build_number = os.environ.get("BUILD_NUMBER", "local")
title = f"Jenkins Run #{build_number}"

# Собираем все result.json файлы
results = []
for f in sorted(glob.glob(f"{results_dir}/*-result.json")):
    try:
        with open(f, 'r', encoding='utf-8') as file:
            data = json.load(file)
            results.append(data)
    except Exception as e:
        print(f"⚠️ Ошибка чтения {f}: {e}")

if not results:
    print("❌ Нет валидных результатов для отправки")
    sys.exit(1)

# Формируем запрос согласно документации DoQA
payload = {
    "token": token,
    "title": title,
    "spaceId": space_id,
    "results": results
}

print(f"🚀 Отправка {len(results)} тестов в DoQA...")

# Отправляем на ПРАВИЛЬНЫЙ эндпоинт
import urllib.request
import urllib.error

url = "https://o7g195.doqa.app/api/runs/from-autotest-report"
req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode('utf-8'),
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    },
    method="POST"
)

try:
    with urllib.request.urlopen(req) as response:
        body = response.read().decode('utf-8')
        print(f"✅ Ответ сервера: {body}")
except urllib.error.HTTPError as e:
    print(f"❌ HTTP {e.code}: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"❌ Ошибка отправки: {e}")
PYEOF

                    python3 send_to_doqa.py
                else
                    echo "❌ Нет JSON-файлов в doqa-results. Проверьте настройки doqa.properties"
                fi

                # Генерация Allure-отчета для Jenkins (опционально)
                if [ -d "allure-results" ]; then
                    /home/ubuntu/jenkins/tools/org.allurereport.jenkins.tools.AllureCommandlineInstallation/allure/bin/allure \
                        generate allure-results -c -o allure-report || echo "⚠️ Не удалось сгенерировать отчет"
                fi
            '''

            archiveArtifacts artifacts: 'doqa-results/*.json', allowEmptyArchive: true
        }
    }
}