# Kube Manager

HTTP service that allows applying, listing, and deleting Kubernetes resources via REST requests. It uses Kubernetes' dynamic client (`client-go`) to handle various resource types without requiring type-specific definitions.

## Available Endpoints

### `POST /deploy`

Applies a YAML manifest to the cluster.

- **Headers**:  
  `Content-Type: text/yaml` or `application/x-yaml`
  
- **Body**:  
  A valid YAML manifest of a Kubernetes resource.

- **Response (200 OK)**:  
  ```
  YAML successfully deployed
  ```

- **Example with curl**:

  ```bash
  curl -X POST http://localhost:8080/deploy        -H "Content-Type: text/yaml"        --data-binary @deployment.yaml
  ```

---

### `GET /list?resource=<type>&namespace=<ns>`

Lists the names of resources of the specified type in an optional namespace.

- **Parameters**:
  - `resource`: the type of resource (e.g., `Deployment`, `Service`, `ConfigMap`, etc.)
  - `namespace` *(optional)*: the namespace to search in (defaults to all if applicable)

- **Response**:  
  A JSON array containing the names of the resources.

- **Example**:

  ```bash
  curl "http://localhost:8080/list?resource=Pod&namespace=default"
  ```

---

### `DELETE /resource?type=<type>&name=<name>&namespace=<ns>`

Deletes a specific resource from the cluster.

- **Parameters**:
  - `type`: resource type (`Deployment`, `Namespace`, `Secret`, etc.)
  - `name`: name of the resource to delete
  - `namespace`: required for namespaced resources (omit for `Namespace`, `ClusterRole`, etc.)

- **Response (204 No Content)**:  
  Indicates the resource was successfully deleted.

- **Example**:

  ```bash
  curl -X DELETE "http://localhost:8080/resource?type=Service&name=nginx-service&namespace=default"
  ```

---

## Supported Resource Types

This service supports the following resource types:

- `Pod`
- `Deployment`
- `Service`
- `Namespace`
- `HorizontalPodAutoscaler`
- `ConfigMap`
- `Secret`
- `PersistentVolumeClaim`
- `Ingress`
- `ServiceAccount`
- `Role`, `RoleBinding`
- `ClusterRole`, `ClusterRoleBinding`
- `NetworkPolicy`
