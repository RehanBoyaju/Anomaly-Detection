import math
import csv
from typing import List, Optional


class Point:
    def __init__(self, *coords: float, metadata: Optional[dict] = None):
        self.coords = list(coords)
        self.visited = False
        self.cluster_id = 0  # 0 = unclassified, -1 = noise
        self.metadata = metadata or {}  # Store additional info like date, transactions, etc.


class Algo:
    """DBSCAN: Density-Based Spatial Clustering of Applications with Noise"""

    def __init__(self, eps: float, min_pts: int):
        self.eps = eps
        self.min_pts = min_pts
        self.points: List[Point] = []

    def add_point(self, *coords: float, metadata: Optional[dict] = None) -> None:
        """Add a point to the dataset"""
        self.points.append(Point(*coords, metadata=metadata))

    def run(self) -> None:

        cluster_id = 0
        for p in self.points:
            if p.visited:
                continue
            p.visited = True
            neighbors = self._region_query(p)
            if len(neighbors) < self.min_pts:
                p.cluster_id = -1  # noise
            else:
                cluster_id += 1
                self._expand_cluster(p, neighbors, cluster_id)

    def _expand_cluster(self, p: Point, neighbors: List[Point], cluster_id: int) -> None:
        p.cluster_id = cluster_id
        i = 0
        while i < len(neighbors):
            np = neighbors[i]
            if not np.visited:
                np.visited = True
                np_neighbors = self._region_query(np)
                if len(np_neighbors) >= self.min_pts:
                    neighbors.extend(np_neighbors)
            if np.cluster_id == 0:
                np.cluster_id = cluster_id
            i += 1

    def _region_query(self, p: Point) -> List[Point]:
        result = []
        for q in self.points:
            if self._euclidean_distance(p, q) <= self.eps:
                result.append(q)
        return result

    def _euclidean_distance(self, a: Point, b: Point) -> float:
        sum_sq = 0.0
        for i in range(len(a.coords)):
            diff = a.coords[i] - b.coords[i]
            sum_sq += diff * diff
        return math.sqrt(sum_sq)

    def get_clusters(self) -> List[List[Point]]:
        clusters = []
        for p in self.points:
            if p.cluster_id > 0:
                self._ensure_cluster_size(clusters, p.cluster_id)
                clusters[p.cluster_id - 1].append(p)
        return clusters

    def _ensure_cluster_size(self, clusters: List[List[Point]], cluster_id: int) -> None:
        while len(clusters) < cluster_id:
            clusters.append([])

    def get_noise(self) -> List[Point]:
        return [p for p in self.points if p.cluster_id == -1]

    def get_cluster_labels(self) -> List[int]:
        return [p.cluster_id for p in self.points]


def load_csv_data(filename: str, features: List[str]) -> Algo:
    """Load CSV data and create DBSCAN points"""
    dbscan = Algo(eps=0.5, min_pts=5)  # Adjust parameters as needed

    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Extract features for clustering
            coords = []
            for feature in features:
                # Handle potential empty or invalid values
                try:
                    value = float(row[feature]) if row[feature] else 0
                    coords.append(value)
                except (ValueError, KeyError):
                    coords.append(0)

            # Store metadata for analysis
            metadata = {
                'date': row.get('Date', ''),
                'transactions': float(row.get('Total Transactions', 0)),
                'traded_shares': float(row.get('Total Traded Shares', 0)),
                'traded_amount': float(row.get('Total Traded Amount', 0)),
                'max_price': float(row.get('Max. Price', 0)),
                'min_price': float(row.get('Min. Price', 0)),
                'close_price': float(row.get('Close Price', 0))
            }

            dbscan.add_point(*coords, metadata=metadata)

    return dbscan


def normalize_data(dbscan: Algo) -> Algo:
    """Normalize the data to improve DBSCAN performance"""
    if not dbscan.points:
        return dbscan

    # Find min and max for each dimension
    dims = len(dbscan.points[0].coords)
    mins = [float('inf')] * dims
    maxs = [float('-inf')] * dims

    for point in dbscan.points:
        for i in range(dims):
            mins[i] = min(mins[i], point.coords[i])
            maxs[i] = max(maxs[i], point.coords[i])

    # Normalize each point
    for point in dbscan.points:
        normalized_coords = []
        for i in range(dims):
            if maxs[i] - mins[i] > 0:
                normalized_coords.append((point.coords[i] - mins[i]) / (maxs[i] - mins[i]))
            else:
                normalized_coords.append(0)
        point.coords = normalized_coords

    return dbscan


def analyze_market_data(dbscan: Algo):
    """Analyze and visualize market data clusters"""
    dbscan.run()

    clusters = dbscan.get_clusters()
    noise = dbscan.get_noise()

    print(f"\n{'='*60}")
    print(f"DBSCAN Analysis Results")
    print(f"{'='*60}")
    print(f"Total points analyzed: {len(dbscan.points)}")
    print(f"Number of clusters found: {len(clusters)}")
    print(f"Noise points: {len(noise)} ({len(noise)/len(dbscan.points)*100:.1f}%)")

    # Analyze each cluster
    for i, cluster in enumerate(clusters):
        print(f"\n{'─'*40}")
        print(f"Cluster {i+1} Characteristics ({len(cluster)} days):")
        print(f"{'─'*40}")

        # Calculate statistics for this cluster
        close_prices = [p.metadata.get('close_price', 0) for p in cluster]
        transactions = [p.metadata.get('transactions', 0) for p in cluster]
        traded_amounts = [p.metadata.get('traded_amount', 0) for p in cluster]

        print(f"  Avg Close Price: Rs{sum(close_prices)/len(close_prices):.2f}")
        print(f"  Price Range: Rs{min(close_prices):.2f} - Rs{max(close_prices):.2f}")
        print(f"  Avg Daily Transactions: {sum(transactions)/len(transactions):.0f}")
        print(f"  Avg Traded Amount: Rs{sum(traded_amounts)/len(traded_amounts):,.0f}")

        # Show sample dates
        dates = [p.metadata.get('date', '') for p in cluster[:3]]
        print(f"  Sample Dates: {', '.join(dates)}")

    # Analyze noise points (unusual trading days)
    if noise:
        print(f"\n{'─'*40}")
        print(f"Unusual Trading Days ({len(noise)} days):")
        print(f"{'─'*40}")
        for p in noise[:10]:  # Show first 10 noise points
            date = p.metadata.get('date', 'Unknown')
            close = p.metadata.get('close_price', 0)
            transactions = p.metadata.get('transactions', 0)
            print(f"  {date}: Close=Rs{close:.2f}, Transactions={transactions:.0f}")

    return clusters, noise

def main():
    # Load and analyze the CSV data
    csv_file = "CMF2_2000-01-01_2021-12-31.csv"

    print("Loading market data...")

    # Choose features for clustering
    # Option 1: Use trading volume and price features
    features = ['Total Transactions', 'Close Price']

    # Option 2: Use multiple features (uncomment for more complex analysis)
    # features = ['Total Transactions', 'Total Traded Shares', 'Close Price', 'Max. Price', 'Min. Price']

    # Load data
    dbscan = load_csv_data(csv_file, features)
    print(f"Loaded {len(dbscan.points)} trading days")

    # Normalize data for better clustering
    print("Normalizing data...")

    # Run DBSCAN with different parameters to find optimal clustering
    print("\n" + "="*60)
    print("Running DBSCAN Analysis")
    print("="*60)

    # Try different parameters
    param_sets = [
        (0.3, 5, "Conservative"),
        (0.5, 5, "Moderate"),
        (0.7, 3, "Aggressive")
    ]

    best_dbscan = None
    best_score = -1

    for eps, min_pts, description in param_sets:
        print(f"\nTrying {description} parameters: eps={eps}, min_pts={min_pts}")

        # Create fresh instance
        test_dbscan = Algo(eps, min_pts)

        # Re-add points with normalized coordinates
        for point in dbscan.points:
            test_dbscan.add_point(*point.coords, metadata=point.metadata)

        # Run clustering
        test_dbscan.run()

        clusters = test_dbscan.get_clusters()
        noise = test_dbscan.get_noise()

        # Calculate a simple score (more clusters with less noise is better)
        if clusters:
            score = len(clusters) * (1 - len(noise)/len(test_dbscan.points))
            print(f"  Clusters: {len(clusters)}, Noise: {len(noise)} ({len(noise)/len(test_dbscan.points)*100:.1f}%), Score: {score:.2f}")

            if score > best_score:
                best_score = score
                best_dbscan = test_dbscan

    # Use the best parameters
    if best_dbscan:
        print(f"\n{'='*60}")
        print(f"Using best parameters for final analysis")
        print(f"{'='*60}")

        # Analyze results
        clusters, noise = analyze_market_data(best_dbscan)

    else:
        print("No valid clusters found. Try adjusting parameters.")


if __name__ == "__main__":
    main()