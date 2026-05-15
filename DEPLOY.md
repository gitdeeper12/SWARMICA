# 🚀 Deployment Guide for NEUROPIA (E-LAB-10)

## Package Deployment (PyPI)

### Prerequisites
```bash
pip install build twine
```

Build Package

```bash
python -m build
```

Upload to PyPI (Production)

```bash
twine upload dist/*
```

---

Docker Deployment

Build Image

```bash
docker build -t neuropia:latest .
```

Run Container

```bash
docker run -it --rm neuropia:latest --regime full_fusion_plant --steps 1000
```

---

CI/CD Pipeline (GitLab CI)

The .gitlab-ci.yml includes:

1. Test - Run unit tests on Python 3.11-3.12
2. Build - Create PyPI package
3. Deploy - Auto-deploy to PyPI on tags

Trigger Deployment

```bash
git tag v1.0.0
git push origin v1.0.0
```

---

Netlify Deployment (Documentation)

```bash
cd Netlify/
netlify deploy --prod
```

Configuration

· Site name: neuropia-v1.netlify.app
· Publish directory: Netlify/

---

Repository Mirrors

```bash
git push github main
git push gitlab main
git push bitbucket main
git push codeberg main
```

---

Verification

```bash
pip install neuropia-engine
curl https://doi.org/10.5281/zenodo.20092199
curl https://neuropia-v1.netlify.app
```

---

FPGA Deployment (TensorRT)

```bash
# Export to TensorRT INT8
python -m neuropia.export_tensorrt --precision int8 --target versal

# Run on Xilinx Versal
./build/neuropia_trt --regime full_fusion_plant --latency-test
```

---

For production deployments, ensure all tests pass and documentation is up to date.
