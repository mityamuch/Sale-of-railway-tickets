import hazelcast


def get_hazelcast_client():
    client = hazelcast.HazelcastClient(
        cluster_name="cluster-name",
        cluster_members=[
            "10.90.0.2:5701",
            "10.90.0.3:5701",
        ],
        lifecycle_listeners=[
            lambda state: print("Lifecycle event >>>", state),
        ]
    )
    return client


hazelcast_client = get_hazelcast_client()
