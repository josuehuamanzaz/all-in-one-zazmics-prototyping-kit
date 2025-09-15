start the project with compose

```sh
docker compose --profile gpu-nvidia build
```

```sh
docker compose --profile gpu-nvidia up
```

```sh
curl http://localhost:11434/api/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nomic-embed-text",
    "prompt": "Texto de ejemplo para embedding"
  }'

```

(optional) use a template to start working

<img src="README images/image-1.png" alt="alt text" width="600"/>

when you are done working, save your project

<img src="README images/image-2.png" alt="alt text" width="600"/>

Just saving the workflow is ok, but it will only live on your comptuer. To push the workflow to github, go to `localhost:5801` and search for your workflow. Save it. Then you use your git tool to have control over the changes you have made.

<img src="README images/image.png" alt="alt text" width="600"/>

delete everything once you are done

```sh
docker compose --profile gpu-nvidia down
```