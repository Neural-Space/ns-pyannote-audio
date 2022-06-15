.PHONY: verify-version-tag
verify-version-tag:
	PYTHONPATH='./src/' python setup.py verify


.PHONY: setup-PYPI-credentials
setup-PYPI-credentials:
	echo "[distutils]" >> ~/.pypirc
	echo "Index-servers = neuralspace" >> ~/.pypirc
	echo "[neuralspace]" >> ~/.pypirc
	echo "Repository = https://europe-west2-python.pkg.dev/platform-staging-319707/neuralspace/" >> ~/.pypirc
	echo "username = $$NS_PYPI_USERNAME" >> ~/.pypirc
	echo "password = $$NS_PYPI_PASSWORD" >> ~/.pypirc


# upload package to private pypi server
.PHONY: package-upload
package-upload:
	if [ -d "./build" ]; then rm -rf "./build"; fi
	if [ -d "./dist" ]; then rm -rf "./dist"; fi
	if [ -d "./src/pyannote.audio.egg-info" ]; then rm -rf "./src/pyannote.audio.egg-info"; fi

	PYTHONPATH='./src/' python setup.py sdist bdist_wheel
	twine upload -r neuralspace dist/*

	if [ -d "./build" ]; then rm -rf ./build; fi
	if [ -d "./dist" ]; then rm -rf ./dist; fi
	if [ -d "./src/pyannote.audio.egg-info" ]; then rm -rf ./src/pyannote.audio.egg-info; fi