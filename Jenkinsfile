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
                    echo " Запускаем Playwright-контейнер..."

                    # Флаг -u $(id -u):$(id -g) решает проблему с правами (Operation not permitted)
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
                        # Удаляем служебные файлы, которые не нужны в сыром отчете
                        rm -f allure-results/testrun.json allure-results/executor.json || true
                        rm -rf allure-results/history || true

                        # ВАЖНО: Зипуем САМУ ПАПКУ allure-results/, чтобы она была корнем архива
                        # Это соответствует требованию DoQA: "Allure (сырые данные... помещенные в архив)"
                        zip -r allure-results.zip allure-results/

                        echo "✅ Архив allure-results.zip успешно создан с правильной структурой"
                    else
                        echo "⚠️ Папка allure-results пуста или отсутствует."
                        echo "⚠️ Создаем фиктивный архив, чтобы curl не упал с ошибкой (26)."
                        mkdir -p allure-results
                        echo '{"status": "empty", "message": "No tests were executed"}' > allure-results/empty.json
                        zip -r allure-results.zip allure-results/
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
                        -F "type=allure" || echo "⚠️ Не удалось отправить отчет (проверьте токен или сеть)"
                else
                    echo "❌ Файл allure-results.zip не найден, отправка пропущена."
                fi
            '''

            // Показываем красивый отчет прямо в интерфейсе Jenkins
            allure results: [[path: 'allure-results']]
        }

        failure {
            echo "❌ Сборка завершилась с ошибкой. Проверьте логи выше."
        }
    }
}