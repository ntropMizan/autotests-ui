pipeline {
    agent { label 'docker-vm' }

    environment {
        DOQA_URL = "https://o7g195.doqa.app"
        DOQA_SPACE_ID = "2"
        // Токен берется из Jenkins Credentials (Secret Text)
        DOQA_TOKEN = credentials('DOQA_TOKEN')
    }

    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }

        stage('Clean Workspace') {
            steps {
                sh '''
                    echo "🧹 Очищаем воркспейс..."
                    rm -rf .pytest_cache allure-results allure-report doqa-results
                    echo "✅ Очистка завершена"
                '''
            }
        }

        stage('Run Playwright Tests') {
            steps {
                sh '''
                    echo " Запускаем тесты в файловом режиме DoQA..."
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
                if [ -d "allure-results" ] && [ "$(ls -A allure-results/*-result.json 2>/dev/null)" ]; then
                    echo "📦 Архивируем результаты..."
                    zip -r allure-results.zip allure-results/

                    echo "🚀 Отправляем в DoQA через API..."
                    curl -X POST https://o7g195.doqa.app/api/autotests/report \
                        -F "token=${DOQA_TOKEN}" \
                        -F "spaceId=2" \
                        -F "file=@allure-results.zip" \
                        -F "type=allure" || echo "⚠️ Ошибка отправки в DoQA"
                else
                    echo "❌ Нет JSON-файлов в allure-results. Проверьте настройки плагина."
                fi

                # Генерация Allure-отчета для Jenkins
                if [ -d "allure-results" ]; then
                    allure generate allure-results -c -o allure-report
                fi
            '''

            // Стандартная архивация артефактов Jenkins
            archiveArtifacts artifacts: 'allure-results.zip', allowEmptyArchive: true
        }
    }
}