pipeline {
    agent { label 'docker-vm' }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Clean Workspace') {
            steps {
                sh '''
                    echo "🧹 Очищаем воркспейс от кэша и старых отчетов..."
                    rm -rf .pytest_cache allure-results allure-report
                    echo "✅ Очистка завершена"
                '''
            }
        }

        stage('Run Playwright Tests') {
            steps {
                sh '''
                    echo "🚀 Запускаем Playwright-контейнер..."

                    # Флаг -u $(id -u):$(id -g) решает проблему с правами доступа
                    docker run --rm --ipc=host -u $(id -u):$(id -g) -v ${WORKSPACE}:/app \
                        my-playwright:latest \
                        pytest . --alluredir=/app/allure-results --cache-clear -v --maxfail=5
                '''
            }
        }

        stage('Prepare Allure Results') {
            steps {
                sh '''
                    echo "📦 Архивируем результаты для DoQA..."

                    if [ -d "allure-results" ] && [ "$(ls -A allure-results)" ]; then
                        # ⚠️ ВАЖНО: НЕ удаляем executor.json и testrun.json!
                        # DoQA требует их наличия для корректного парсинга прогона.

                        # Заходим внутрь папки и зипуем СОДЕРЖИМОЕ (точка означает "текущая папка")
                        # Файлы будут лежать в корне архива, без лишней обертки allure-results/
                        cd allure-results && zip -r ../allure-results.zip . && cd ..

                        echo "✅ Архив allure-results.zip успешно создан (файлы в корне, служебные файлы сохранены)"
                    else
                        echo "⚠️ Папка allure-results пуста или отсутствует."
                        mkdir -p allure-results
                        echo '{"name": "empty", "status": "broken"}' > allure-results/empty-result.json
                        cd allure-results && zip -r ../allure-results.zip . && cd ..
                    fi
                '''
            }
        }
    }

    post {
        always {
            sh '''
                echo "📤 Отправляем отчет в DoQA (официальный API v4.0)..."
                if [ -f "allure-results.zip" ]; then
                    # Используем официальный эндпоинт /api/autotests/report
                    # Токен передается ТОЛЬКО в теле формы, как указано в доке
                    curl -X POST https://o7g195.doqa.app/api/autotests/report \
                        -F "token=d5c53a9c-bd1c-41e9-bdb0-9766864bb207" \
                        -F "spaceId=2" \
                        -F "file=@allure-results.zip" \
                        -F "type=allure" || echo "⚠️ Ошибка отправки в DoQA"
                else
                    echo "❌ Файл allure-results.zip не найден, отправка пропущена."
                fi
            '''

            // Генерация отчета для интерфейса Jenkins
            allure results: [[path: 'allure-results']]
        }

        failure {
            echo "❌ Сборка завершилась с ошибкой. Проверьте логи выше."
        }
    }
}