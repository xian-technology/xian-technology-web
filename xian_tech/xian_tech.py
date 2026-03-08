import reflex as rx

from .data import HOME_SOCIAL_META, SOCIAL_PREVIEW_DESCRIPTION, SOCIAL_PREVIEW_IMAGE_URL
from .pages.abci import abci_page
from .pages.consensus import consensus_page
from .pages.contracting import contracting_page
from .pages.home import home_page
from .pages.developers import developers_page
from .pages.api import api_page
from .pages.about import about_page
from .pages.contact import contact_page
from .pages.faq import faq_page
from .pages.node_network import node_network_page
from .pages.roadmap import roadmap_page
from .pages.samples import samples_page
from .pages.tutorials import tutorials_page
from .pages.tooling import tooling_page
from .pages.not_found import not_found_page
from .state import State


app = rx.App(
    theme=rx.theme(appearance="inherit"),
    stylesheets=["/css/site.css"],
    head_components=[
        rx.el.link(rel="icon", type="image/png", href="/favicon.png"),
        rx.el.link(rel="shortcut icon", type="image/png", href="/favicon.png"),
    ],
)

app.add_page(
    home_page,
    route="/",
    title="Xian Technology",
    description=SOCIAL_PREVIEW_DESCRIPTION,
    image=SOCIAL_PREVIEW_IMAGE_URL,
    meta=HOME_SOCIAL_META,
)
app.add_page(consensus_page, route="/consensus", title="CometBFT Consensus")
app.add_page(contracting_page, route="/contracting", title="Contracting")
app.add_page(abci_page, route="/abci", title="ABCI for CometBFT")
app.add_page(tooling_page, route="/tooling", title="Tooling & Integrations")
app.add_page(developers_page, route="/developers", title="Developer Hub")
app.add_page(about_page, route="/about", title="About the Foundation")
app.add_page(faq_page, route="/faq", title="FAQ")
app.add_page(contact_page, route="/contact", title="Contact")
app.add_page(node_network_page, route="/node-network", title="Node & Network")
app.add_page(roadmap_page, route="/roadmap", title="Roadmap", on_load=State.refresh_roadmap)
app.add_page(samples_page, route="/samples", title="Samples & SDKs")
app.add_page(tutorials_page, route="/tutorials", title="Tutorials & First Steps")
app.add_page(api_page, route="/api", title="API References")
app.add_page(not_found_page, route="404", title="404 - Not Found")
