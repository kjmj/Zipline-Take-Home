document.body.addEventListener("htmx:afterRequest", function (event) {
  showAsLRGraph(event);
});

function reRenderMermaidGraph(eltId) {
  const element = document.getElementById(eltId);
  element.classList.add("mermaid");
  element.removeAttribute("data-processed");
  mermaid.contentLoaded();
}

function addClickListenersToNodes(alpineData, id) {
  setTimeout(() => {
    document
      .getElementById(id)
      .querySelectorAll(".node")
      .forEach((node) => {
        node.style.cursor = "pointer";
        const nodeName = node.textContent.trim();
        node.addEventListener("click", (event) => {
          if (id === "full-mermaid-graph") {
            alpineData.clicked = nodeName;
            htmx
              .ajax("GET", `/upstream/${nodeName}`, "#mermaid-graph")
              .then(() => {
                reRenderMermaidGraph("mermaid-graph", alpineData);
                addClickListenersToNodes(alpineData, "mermaid-graph");
              });
          } else if (id === "mermaid-graph") {
            alpineData.nodeDetails = nodeName;
            htmx.ajax("GET", `/nodes/${nodeName}`, "#node-details");
          }
        });
      });
  });
}

function afterRequestResult(alpineData) {
  setTimeout(() => {
    reRenderMermaidGraph("mermaid-graph", alpineData);
  });
  addClickListenersToNodes(alpineData, "mermaid-graph");
}

function showAsLRGraph(event) {
  let response = event.detail.xhr.responseText;
  event.detail.target.innerHTML = "graph LR; " + response;
}
