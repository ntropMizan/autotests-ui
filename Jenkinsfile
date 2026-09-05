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
                    rm -rf .pytest_cache allure-results allure-report doqa-results allure-results.zip
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
                if [ -d "allure-results" ] && [ "$(ls -A allure-results/*-result.json 2>/dev/null)" ]; then
                    echo "📦 Добавляем маркер формата Allure..."
                    # КРИТИЧНО: Без этого файла парсер DoQA отвергает архив
                    cat > allure-results/environment.properties << EOF
reportType=allure
framework=pytest
jenkinsBuild=${BUILD_NUMBER}
EOF

                    echo " Архивируем результаты..."
                    cd allure-results && zip -r ../allure-results.zip . && cd ..

                    echo "🚀 Отправляем в DoQA..."
                    curl -v https://o7g195.doqa.app/api/autotests/report \
                        -H "Authorization: Bearer ${DOQA_TOKEN}" \
                        -F "token=${DOQA_TOKEN}" \
                        -F "spaceId=2" \
                        -F "type=allure" \
                        -F "file=@allure-results.zip" \
                        -F "testRunName=Jenkins Run #${BUILD_NUMBER}" || echo "⚠️ Ошибка отправки"
                else
                    echo "❌ Нет результатов для отправки"
                fi

                # Генерация отчета для Jenkins
                if [ -d "allure-results" ]; then
                    /home/ubuntu/jenkins/tools/org.allurereport.jenkins.tools.AllureCommandlineInstallation/allure/bin/allure \
                        generate allure-results -c -o allure-report || echo "⚠️ Ошибка генерации Allure"
                fi
            '''
            archiveArtifacts artifacts: 'allure-results.zip', allowEmptyArchive: true
        }
    }
}