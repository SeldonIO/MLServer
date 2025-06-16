version=$(sed 's/^__version__ = "\(.*\)"/\1/' ./mlserver/version.py)
tag=${version}-sklearn-$(date '+%Y-%m-%d')
./hack/build-image.sh ${version} sklearn
podman tag localhost/seldonio/mlserver:${version}-sklearn 724664234782.dkr.ecr.us-east-1.amazonaws.com/library/hardened/seldonio/mlserver:${tag}
