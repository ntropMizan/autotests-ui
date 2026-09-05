pipeline {
    agent { label 'docker-vm' }

    environment {
        DOQA_URL = "https://o7g195.doqa.app"
        DOQA_SPACE_ID = "2"
        // Укажите здесь точный ID вашего Secret Text
        DOQA_TOKEN = credentials('DOQA_TOKEN')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Clean Workspace') {
            steps {
                sh '''
                    echo " Очищаем воркспейс..."
                    rm -rf .pytest_cache allure-results allure-report doqa-results
                    echo "✅ Очистка завершена"
                '''
            }
        }

        stage('Run Playwright Tests with DoQA') {
            steps {
                sh '''
                    echo " Запускаем тесты с нативной интеграцией DoQA..."

                    docker run --rm --ipc=host -u $(id -u):$(id -g) \
                        -v ${WORKSPACE}:/app \
                        -e DOQA_URL=${DOQA_URL} \
                        -e DOQA_TOKEN=${DOQA_TOKEN} \
                        -e DOQA_SPACE_ID=${DOQA_SPACE_ID} \
                        my-playwright:latest \
                        pytest . --cache-clear -v --maxfail=5
                '''
            }
        }
    }

    post {
        always {
            script {
                // Генерация локального Allure-отчета для просмотра в Jenkins
                if (fileExists('allure-results')) {
                    allure results: [[path: 'allure-results']]
                } else {
                    echo "⚠️ Папка allure-results не найдена. Проверьте настройки doqa-pytest."
                }
            }
        }

        failure {
            echo "❌ Сборка завершилась с ошибкой. Результаты уже отправлены в DoQA (если сеть была доступна)."
        }
    }
}