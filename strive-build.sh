pushd runtimes/huggingface
poetry lock --no-update
popd

pushd runtimes/sklearn
poetry lock --no-update
popd

poetry lock --no-update

version=$(sed 's/^__version__ = "\(.*\)"/\1/' ./mlserver/version.py)
tag=${version}-sklearn-$(date '+%Y-%m-%d')
./hack/build-image.sh ${version} sklearn || true
podman tag localhost/seldonio/mlserver:${version}-sklearn 724664234782.dkr.ecr.us-east-1.amazonaws.com/library/hardened/seldonio/mlserver:${tag}
