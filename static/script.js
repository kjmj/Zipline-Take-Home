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
        node.addEventListener("click", () => {
          if (id === "full-mermaid-graph") {
            showUpstreamGraph(nodeName, alpineData);
          } else if (id === "mermaid-graph") {
            showDetailSidebar(nodeName, alpineData);
          }
        });
      });
  });
}

function showDetailSidebar(nodeName, alpineData) {
  alpineData.clicked = nodeName;
  alpineData.nodeDetails = nodeName;
  htmx.ajax("GET", `/nodes/${nodeName}`, "#node-details");
}

function showUpstreamGraph(nodeName, alpineData) {
  alpineData.clicked = nodeName;
  htmx.ajax("GET", `/upstream/${nodeName}`, "#mermaid-graph").then(() => {
    reRenderMermaidGraph("mermaid-graph", alpineData);
    addClickListenersToNodes(alpineData, "mermaid-graph");
  });
}

function showAsLRGraph(event) {
  let response = event.detail.xhr.responseText;
  event.detail.target.innerHTML = "graph LR; " + response;
}
