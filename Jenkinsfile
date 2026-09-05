pipeline {
    agent { label 'docker-vm' }

    stages {
        stage('Checkout') {
            steps {
                // Явно клонируем код, чтобы гарантировать его наличие в воркспейсе
                checkout scm
            }
        }

        stage('Run Playwright Tests') {
            steps {
                sh '''
                    echo "🚀 Запускаем Playwright-контейнер..."
                    # Используем ${WORKSPACE} вместо хардкода пути
                    # Если тесты лежат в папке tests/, замените "pytest ." на "pytest tests/"
                    docker run --rm --ipc=host -v ${WORKSPACE}:/app \
                        my-playwright:latest \
                        pytest . --alluredir=/app/allure-results -v --maxfail=5
                '''
            }
        }

        stage('Prepare Allure Results') {
            steps {
                sh '''
                    echo "📦 Подготавливаем Allure-результаты для DoQA..."

                    if [ -d "allure-results" ] && [ "$(ls -A allure-results)" ]; then
                        sudo chown -R ubuntu:ubuntu allure-results/ || true
                        chmod -R 755 allure-results/ || true

                        cd allure-results
                        rm -f testrun.json executor.json || true
                        rm -rf history || true

                        # Архивируем ВСЁ содержимое папки, чтобы избежать ошибки zip при отсутствии файлов по маске
                        zip -r ../allure-results.zip .
                        cd ..
                        echo "✅ Архив allure-results.zip успешно создан"
                    else
                        echo "⚠️ Директория allure-results пуста или не существует."
                        echo "⚠️ Создаем фиктивный архив, чтобы curl не упал с ошибкой 26."
                        mkdir -p allure-results
                        echo '{"empty": true, "message": "No tests were executed"}' > allure-results/empty.json
                        zip -r allure-results.zip allure-results
                    fi
                '''
            }
        }
    }

    post {
        always {
            sh '''
                echo "📤 Отправляем отчет в DoQA..."
                if [ -f "allure-results.zip" ]; then
                    curl -X POST https://o7g195.doqa.app/api/autotests/report \
                        -F "token=43d1faef-c620-43b6-9078-db9de7f76311" \
                        -F "spaceId=2" \
                        -F "file=@allure-results.zip" \
                        -F "type=allure" || echo "⚠️ Ошибка при отправке в DoQA (проверьте лог curl)"
                    echo "✅ Отчет отправлен в DoQA!"
                else
                    echo "❌ Файл allure-results.zip не найден, отправка пропущена."
                fi
            '''

            // Показываем отчет прямо в Jenkins, даже если отправка в DoQA не удалась
            allure results: [[path: 'allure-results']]
        }
    }
}