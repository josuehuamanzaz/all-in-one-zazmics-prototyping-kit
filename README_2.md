```sh
docker compose --profile gpu-nvidia build
```

```sh
docker compose --profile gpu-nvidia up
```

add the `nomic-embed-text` model to create embedding

```sh
docker exec -it ollama ollama pull nomic-embed-text
```

```sh
curl http://ollama:11434/api/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nomic-embed-text",
    "prompt": "Texto de ejemplo para embedding"
  }'

```

```sh
docker exec -it extract-workflow sh -c "cd /workspace/borra && python temp.py"
```

```sh
docker compose down -v
```