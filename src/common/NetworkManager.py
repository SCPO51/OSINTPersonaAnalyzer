from pyvis.network import Network


class NetworkManager:
    def __init__(self, height=None):
        if height:
            self.network = Network(height=height)
        else:
            self.network = Network()
        self.label_to_id = {}
        self.current_id = 1

    def add_node(self, label, link, color=None):
        if label not in self.label_to_id:
            self.label_to_id[label] = self.current_id
            self.network.add_node(self.current_id, label=label, color=color, title=link)
            self.current_id += 1

    def add_edge(self, source_label, target_label):
        if source_label not in self.label_to_id:
            self.add_node(source_label)
        if target_label not in self.label_to_id:
            self.add_node(target_label)

        self.network.add_edge(
            self.label_to_id[source_label], self.label_to_id[target_label]
        )

    def generate_html(self):
        html = self.network.generate_html()
        html = html.replace(
            "</body>",
            """
            <script>
            document.addEventListener("DOMContentLoaded", function() {
                network.on("click", function(params) {
                    if(params.nodes.length > 0) {
                        const node = nodes.get(params.nodes[0]);
                        navigator.clipboard.writeText(node.title);
                    }
                });
            });
            </script>
            </body>
            """,
        )
        return html

    def get_node_ids(self):
        return list(self.label_to_id.values())

    def save_html(self, file_path):
        html = self.generate_html()
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)


if __name__ == "__main__":
    net = NetworkManager()
    net.add_node("test", "original", "orange")
    net.add_node("test1", "original", "orange")
    net.add_edge("test", "test1")
    net.save_html("test.html")
