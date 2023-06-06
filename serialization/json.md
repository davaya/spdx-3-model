# JSON Serialization

As described in [Logical Values](logical/README.md), JSON is a general purpose data format
that does not depend upon data objects being graph nodes, define RDF-based reserved
property names (@id, @type, @graph, etc.), or require applications to perform
RDF-specific processing of JSON data.

Individual SPDX v3 Elements serialized in JSON format can be read directly into
application variables (mapping types and array types) available in most programming
languages, and correspond directly to the logical values of those Elements. A defined
algorithm combines an arbitrary set of logical Elements into a single JSON payload
without regard to the content of those elements. The algorithm performs two operations:
1) factor out shared payload namespaces from all element IDs using namespaceMap
2) factor out shared CreationInformation into a single copy

These operations are reversed when a payload is de-serialized into the original set
of logical Elements, and unlike a general-purpose lossless compression algorithm, yield
a payload that is both compact and human-readable.

For example, a JSON-LD Person element may look like:
```json
{
  "@context": "https://spdx.github.io/spdx-3-model/rdf/context.json",
  "@graph": [
    {
      "@type": "Person",
      "@id": "https://some.namespace#john_smith",
      "creationInfo": {
        "specVersion": "3.0.0",
        "created": "2022-12-01T00:00:00",
        "createdBy": [
          "https://some.namespace#john_smith"
        ],
        "profile": [
          "core"
        ],
        "dataLicense": "CC0-1.0"
      },
      "name": "John Smith",
      "externalIdentifier": [
        {
          "@type": "ExternalIdentifier",
          "externalIdentifierType": "email",
          "identifier": "john@smith.com"
        }
      ]
    }
  ]
}
```
This would be deserialized into the logical value:
```
                             SPDXID = 'https://some.namespace#john_smith'
                               name = 'John Smith'
           creationInfo.specVersion = 'v3.0.0'
             creationInfo.profile.0 = 'core'
               creationInfo.created = '2022-12-01T00:00:00'
           creationInfo.dataLicense = 'CC0-1.0'
           creationInfo.createdBy.0 = 'https://some.namespace#john_smith'
externalIdentifier.0.externalIdentifierType = 'email'
    externalIdentifier.0.identifier = 'john@smith.com'
```
which would then be serialized into JSON:
```json
{
  "SPDXID": "https://some.namespace#john_smith",
  "type": {
    "person": {}
  },
  "name": "John Smith",
  "creationInfo": {
    "specVersion": "v3.0.0",
    "profile": ["core"],
    "created": "2022-12-01T00:00:00",
    "dataLicense": "CC0-1.0",
    "createdBy": ["https://some.namespace#john_smith"]
  },
  "externalIdentifier": [
    {
      "externalIdentifierType": "email",
      "identifier": "john@smith.com"
    }
  ]
}
```
