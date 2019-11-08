export version=test-multi-version
[ -z "$version" ] && gcloud app deploy --quiet || gcloud app deploy app.yaml --version $version --quiet