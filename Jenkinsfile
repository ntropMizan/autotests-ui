pipeline {
    agent { label 'docker-vm' }

    environment {
        DOQA_URL = "https://o7g195.doqa.app"
        DOQA_SPACE_ID = "2"
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
                    rm -rf .pytest_cache allure-results allure-report doqa-results doqa-results.zip
                    echo "✅ Очистка завершена"
                '''
            }
        }

        stage('Run Playwright Tests') {
            steps {
                sh '''
                    echo "🚀 Запускаем тесты в файловом режиме DoQA..."
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
                # 1. Отправка НАТИВНЫХ результатов DoQA (без type=allure!)
                if [ -d "doqa-results" ] && [ "$(ls -A doqa-results/*.json 2>/dev/null)" ]; then
                    echo "📦 Архивируем нативные результаты..."
                    cd doqa-results && zip -r ../doqa-results.zip . && cd ..

                    echo "🚀 Отправляем в DoQA..."
                    curl -v https://o7g195.doqa.app/api/autotests/report \
                        -H "Authorization: Bearer ${DOQA_TOKEN}" \
                        -F "token=${DOQA_TOKEN}" \
                        -F "spaceId=2" \
                        -F "file=@doqa-results.zip" \
                        -F "testRunName=Jenkins Run #${BUILD_NUMBER}" || echo "️ Ошибка отправки"
                else
                    echo "❌ Нет JSON-файлов в doqa-results. Проверьте настройки плагина."
                fi

                # 2. Генерация Allure-отчета для Jenkins (опционально)
                if [ -d "allure-results" ]; then
                    /home/ubuntu/jenkins/tools/org.allurereport.jenkins.tools.AllureCommandlineInstallation/allure/bin/allure \
                        generate allure-results -c -o allure-report || echo "⚠️ Не удалось сгенерировать отчет"
                fi
            '''

            archiveArtifacts artifacts: 'doqa-results.zip', allowEmptyArchive: true
        }
    }
}