import java.awt.Color;
import java.awt.Font;
import java.awt.GraphicsEnvironment;
import java.io.File;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

import org.gephi.graph.api.Edge;
import org.gephi.graph.api.Graph;
import org.gephi.graph.api.GraphController;
import org.gephi.graph.api.GraphModel;
import org.gephi.graph.api.Node;
import org.gephi.io.exporter.api.ExportController;
import org.gephi.io.exporter.preview.PNGExporter;
import org.gephi.io.importer.api.Container;
import org.gephi.io.importer.api.EdgeDirectionDefault;
import org.gephi.io.importer.api.ImportController;
import org.gephi.io.importer.plugin.file.spreadsheet.ImporterSpreadsheetCSV;
import org.gephi.io.importer.plugin.file.spreadsheet.process.SpreadsheetGeneralConfiguration;
import org.gephi.io.processor.plugin.AppendProcessor;
import org.gephi.io.processor.plugin.DefaultProcessor;
import org.gephi.layout.plugin.forceAtlas2.ForceAtlas2;
import org.gephi.layout.plugin.forceAtlas2.ForceAtlas2Builder;
import org.gephi.preview.api.PreviewController;
import org.gephi.preview.api.PreviewModel;
import org.gephi.preview.api.PreviewProperties;
import org.gephi.preview.api.PreviewProperty;
import org.gephi.preview.types.DependantColor;
import org.gephi.preview.types.DependantOriginalColor;
import org.gephi.preview.types.EdgeColor;
import org.gephi.project.api.ProjectController;
import org.gephi.project.api.Workspace;
import org.openide.util.Lookup;

/**
 * Headless Gephi (Gephi Toolkit 0.11.3) run for the company-case network on slide S9.
 * Imports nodes.csv and edges.csv, runs ForceAtlas 2 (prevent overlap), colours nodes by Role and edges by Status,
 * and exports PNG and SVG with the Preview module, plus the .gephi project.
 *
 * args: nodes.csv edges.csv outPrefix widthPx heightPx excludeIds(comma, or -) fontDir seed labelPx edgeLabelPx [scaling gravity strongGravity nodeSize]
 */
public class RenderNetwork {

    static final Map<String, String> NODE_LABELS = new HashMap<>();
    static final Map<String, String> EDGE_LABELS = new HashMap<>();
    static {
        NODE_LABELS.put("vw", "Volkswagen");
        NODE_LABELS.put("stegra", "Stegra");
        NODE_LABELS.put("aid", "State aid (EU-approved)");
        // short edge labels from the Status and Date columns of edges.csv (aid dates from the outline: 20 Jul 2023, 4 Oct 2022)
        EDGE_LABELS.put("1", "MoU 2024 (plan)");
        EDGE_LABELS.put("2", "Contract 2026");
        EDGE_LABELS.put("3", "Agreement 2023");
        EDGE_LABELS.put("4", "Agreement 2021");
        EDGE_LABELS.put("5", "Early use 2021");
        EDGE_LABELS.put("6", "Aid approved 2023");
        EDGE_LABELS.put("7", "Aid approved 2022");
    }

    /** Hand-placed layout (base canvas 880 x 620 for the S9 cut, 880 x 720 for the full network; y downwards): ForceAtlas 2 turns these three disconnected chains into a hairball. */
    static final Map<String, double[]> POS_MAIN = new HashMap<>();
    static final Map<String, double[]> POS_FULL = new HashMap<>();
    static {
        double[][] left = {{240, 45}, {240, 170}, {240, 295}, {240, 420}, {240, 545}};
        String[] leftIds = {"vw", "tkss", "aid", "sz", "ewe"};
        for (int i = 0; i < 5; i++) { POS_MAIN.put(leftIds[i], left[i]); POS_FULL.put(leftIds[i], left[i]); }
        POS_MAIN.put("mb", new double[]{690, 100}); POS_MAIN.put("stegra", new double[]{690, 295}); POS_MAIN.put("bmw", new double[]{690, 490});
        POS_FULL.put("mb", new double[]{690, 45}); POS_FULL.put("stegra", new double[]{690, 170}); POS_FULL.put("bmw", new double[]{690, 295});
        POS_FULL.put("ssab", new double[]{690, 440}); POS_FULL.put("volvo", new double[]{690, 565}); POS_FULL.put("outo", new double[]{690, 690});
    }

    static Color roleColor(String role) {
        if (role == null) return Color.decode("#78828C");
        switch (role) {
            case "steel producer": return Color.decode("#2B5C98");
            case "steel buyer": return Color.decode("#78828C");
            case "hydrogen supplier": return Color.decode("#167A67");
            case "public funder": return Color.decode("#B26A00");
            default: return Color.decode("#78828C");
        }
    }

    static Color statusColor(String status) {
        if (status == null) return Color.decode("#78828C");
        if (status.startsWith("MoU")) return Color.decode("#B26A00");
        if (status.startsWith("Supply contract")) return Color.decode("#167A67");
        if (status.startsWith("Supply agreement")) return Color.decode("#2B5C98");
        if (status.startsWith("State aid")) return Color.decode("#B26A00");
        return Color.decode("#78828C");
    }

    public static void main(String[] a) throws Exception {
        File nodesCsv = new File(a[0]), edgesCsv = new File(a[1]);
        String prefix = a[2];
        int width = Integer.parseInt(a[3]), height = Integer.parseInt(a[4]);
        Set<String> exclude = a[5].equals("-") ? new HashSet<String>() : new HashSet<String>(Arrays.asList(a[5].split(",")));
        File fontDir = new File(a[6]);
        long seed = Long.parseLong(a[7]);
        float labelPx = Float.parseFloat(a[8]), edgeLabelPx = Float.parseFloat(a[9]);
        double scaling = a.length > 10 ? Double.parseDouble(a[10]) : 40.0;
        double gravity = a.length > 11 ? Double.parseDouble(a[11]) : 1.0;
        boolean strong = a.length > 12 && Boolean.parseBoolean(a[12]);
        float nodeSize = a.length > 13 ? Float.parseFloat(a[13]) : 40f;
        String mode = a.length > 14 ? a[14] : "manual";
        double S = width / 880.0;

        Font regular = Font.createFont(Font.TRUETYPE_FONT, new File(fontDir, "thsarabunnew-webfont.ttf"));
        Font bold = Font.createFont(Font.TRUETYPE_FONT, new File(fontDir, "thsarabunnew_bold-webfont.ttf"));
        GraphicsEnvironment.getLocalGraphicsEnvironment().registerFont(regular);
        GraphicsEnvironment.getLocalGraphicsEnvironment().registerFont(bold);

        ProjectController pc = Lookup.getDefault().lookup(ProjectController.class);
        pc.newProject();
        Workspace workspace = pc.getCurrentWorkspace();
        ImportController ic = Lookup.getDefault().lookup(ImportController.class);

        ImporterSpreadsheetCSV nodesImporter = (ImporterSpreadsheetCSV) ic.getFileImporter(nodesCsv);
        nodesImporter.setMode(SpreadsheetGeneralConfiguration.Mode.NODES_TABLE);
        Container nodesContainer = ic.importFile(nodesCsv, nodesImporter);
        nodesContainer.getLoader().setEdgeDefault(EdgeDirectionDefault.DIRECTED);
        ic.process(nodesContainer, new DefaultProcessor(), workspace);

        ImporterSpreadsheetCSV edgesImporter = (ImporterSpreadsheetCSV) ic.getFileImporter(edgesCsv);
        edgesImporter.setMode(SpreadsheetGeneralConfiguration.Mode.EDGES_TABLE);
        Container edgesContainer = ic.importFile(edgesCsv, edgesImporter);
        edgesContainer.getLoader().setEdgeDefault(EdgeDirectionDefault.DIRECTED);
        ic.process(edgesContainer, new AppendProcessor(), workspace);

        GraphModel gm = Lookup.getDefault().lookup(GraphController.class).getGraphModel(workspace);
        Graph graph = gm.getGraph();
        for (Node n : graph.getNodes().toArray()) {
            if (exclude.contains(String.valueOf(n.getId()))) graph.removeNode(n);
        }
        java.util.Random rnd = new java.util.Random(seed);
        for (Node n : graph.getNodes()) {
            String id = String.valueOf(n.getId());
            n.setColor(roleColor((String) n.getAttribute("Role")));
            n.setSize(nodeSize);
            n.setX((float) (rnd.nextDouble() * 1000 - 500));
            n.setY((float) (rnd.nextDouble() * 1000 - 500));
            n.setSize((float) (nodeSize * S));
            if (NODE_LABELS.containsKey(id)) n.setLabel(NODE_LABELS.get(id));
        }
        for (Edge e : graph.getEdges()) {
            e.setColor(statusColor((String) e.getAttribute("Status")));
            String id = String.valueOf(e.getId());
            if (EDGE_LABELS.containsKey(id)) e.setLabel(EDGE_LABELS.get(id));
        }
        System.out.println("graph: " + graph.getNodeCount() + " nodes, " + graph.getEdgeCount() + " edges");

        if (mode.equals("manual")) {
            Map<String, double[]> pos = exclude.isEmpty() ? POS_FULL : POS_MAIN;
            for (Node n : graph.getNodes()) {
                double[] xy = pos.get(String.valueOf(n.getId()));
                n.setX((float) (xy[0] * S));
                n.setY((float) (-xy[1] * S));
            }
        } else {
        ForceAtlas2 fa2 = new ForceAtlas2(new ForceAtlas2Builder());
        fa2.setGraphModel(gm);
        fa2.resetPropertiesValues();
        fa2.setAdjustSizes(true);
        fa2.setScalingRatio(scaling);
        fa2.setGravity(gravity);
        fa2.setStrongGravityMode(strong);
        fa2.setBarnesHutOptimize(false);
        fa2.setThreadsCount(1);
        fa2.setInitialisationSeed(seed);
        fa2.initAlgo();
        for (int i = 0; i < 3000 && fa2.canAlgo(); i++) fa2.goAlgo();
        fa2.endAlgo();
        }

        PreviewController pvc = Lookup.getDefault().lookup(PreviewController.class);
        PreviewModel pm = pvc.getModel(workspace);
        PreviewProperties p = pm.getProperties();
        p.putValue(PreviewProperty.BACKGROUND_COLOR, Color.WHITE);
        p.putValue(PreviewProperty.MARGIN, 4f);
        p.putValue(PreviewProperty.DIRECTED, Boolean.TRUE);
        p.putValue(PreviewProperty.ARROW_SIZE, (float) (4 * S));
        p.putValue(PreviewProperty.EDGE_CURVED, Boolean.FALSE);
        p.putValue(PreviewProperty.EDGE_COLOR, new EdgeColor(EdgeColor.Mode.ORIGINAL));
        p.putValue(PreviewProperty.EDGE_THICKNESS, (float) (3 * S));
        p.putValue(PreviewProperty.EDGE_RESCALE_WEIGHT, Boolean.FALSE);
        p.putValue(PreviewProperty.EDGE_OPACITY, 100f);
        p.putValue(PreviewProperty.NODE_BORDER_WIDTH, 0f);
        p.putValue(PreviewProperty.SHOW_NODE_LABELS, Boolean.TRUE);
        p.putValue(PreviewProperty.NODE_LABEL_FONT, bold.deriveFont(Font.BOLD, (float) (labelPx * S)));
        p.putValue(PreviewProperty.NODE_LABEL_PROPORTIONAL_SIZE, Boolean.FALSE);
        p.putValue(PreviewProperty.NODE_LABEL_SHORTEN, Boolean.FALSE);
        p.putValue(PreviewProperty.NODE_LABEL_COLOR, new DependantOriginalColor(Color.decode("#263444")));
        p.putValue(PreviewProperty.NODE_OPACITY, 0f);
        p.putValue(PreviewProperty.NODE_LABEL_SHOW_BOX, Boolean.TRUE);
        p.putValue(PreviewProperty.NODE_LABEL_BOX_COLOR, new DependantColor(DependantColor.Mode.PARENT));
        p.putValue(PreviewProperty.NODE_LABEL_BOX_OPACITY, 100f);
        p.putValue(PreviewProperty.NODE_LABEL_OUTLINE_SIZE, 0f);
        p.putValue(PreviewProperty.NODE_LABEL_OUTLINE_COLOR, new DependantColor(Color.WHITE));
        p.putValue(PreviewProperty.SHOW_EDGE_LABELS, Boolean.TRUE);
        p.putValue(PreviewProperty.EDGE_LABEL_FONT, regular.deriveFont(Font.PLAIN, (float) (edgeLabelPx * S)));
        p.putValue(PreviewProperty.EDGE_LABEL_SHORTEN, Boolean.FALSE);
        p.putValue(PreviewProperty.EDGE_LABEL_COLOR, new DependantOriginalColor(Color.decode("#263444")));
        p.putValue(PreviewProperty.EDGE_LABEL_OUTLINE_SIZE, (float) (4 * S));
        p.putValue(PreviewProperty.EDGE_LABEL_OUTLINE_COLOR, new DependantColor(Color.WHITE));
        pvc.refreshPreview(workspace);

        ExportController ec = Lookup.getDefault().lookup(ExportController.class);
        PNGExporter png = (PNGExporter) ec.getExporter("png");
        png.setWorkspace(workspace);
        png.setWidth(width);
        png.setHeight(height);
        png.setTransparentBackground(false);
        ec.exportFile(new File(prefix + ".png"), png);
        ec.exportFile(new File(prefix + ".svg"));
        pc.saveProject(pc.getCurrentProject(), new File(prefix + ".gephi"));
        System.out.println("wrote " + prefix + ".png, .svg, .gephi");
    }
}
