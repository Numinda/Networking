import ns.core
import ns.lte
import ns.network
import ns.mobility
import ns.internet
import ns.point_to_point

# Create nodes for base station and user equipment
ue_node = ns.network.Node()
enb_node = ns.network.Node()

# Install LTE protocol stack on nodes
ue_lte_net_device = ns.lte.LteUeNetDevice()
ue_net_device = ns.internet.PointToPointNetDevice()
ue_node.AddDevice(ue_net_device)
ue_node.AddDevice(ue_lte_net_device)

enb_lte_net_device = ns.lte.LteEnbNetDevice()
enb_net_device = ns.internet.PointToPointNetDevice()
enb_node.AddDevice(enb_net_device)
enb_node.AddDevice(enb_lte_net_device)

# Set up LTE helper
lte_helper = ns.lte.LteHelper()
lte_helper.SetEnbDeviceAttribute("DlEarfcn", ns.core.UintegerValue(50))
lte_helper.SetEnbDeviceAttribute("UlEarfcn", ns.core.UintegerValue(19250))
lte_helper.SetEnbDeviceAttribute("CellId", ns.core.UintegerValue(1))

# Set up mobility model for user equipment
ue_mobility = ns.mobility.MobileNode()
ue_node.AddChild(ue_mobility)

# Set up mobility model for base station
enb_mobility = ns.mobility.MobileNode()
enb_node.AddChild(enb_mobility)

# Set up a point-to-point link between base station and user equipment
point_to_point_helper = ns.point_to_point.PointToPointHelper()
point_to_point_helper.SetDeviceAttribute("DataRate", ns.core.StringValue("5Mbps"))
point_to_point_helper.SetChannelAttribute("Delay", ns.core.TimeValue(ns.core.MilliSeconds(2)))

point_to_point_link = point_to_point_helper.Install(enb_node, ue_node)

# Set up the Internet stack on user equipment
internet_stack = ns.internet.InternetStackHelper()
internet_stack.Install(ue_node)

# Assign IP addresses to devices
ue_ipv4 = ns.internet.Ipv4AddressHelper()
ue_ipv4.SetBase(ns.network.Ipv4Address("10.1.1.0"), ns.network.Ipv4Mask("255.255.255.0"))
ue_ipv4.Assign(ue_net_device)

# Set up routing for user equipment
ue_ipv4_gateway = ns.internet.Ipv4AddressHelper()
ue_ipv4_gateway.SetBase(ns.network.Ipv4Address("10.1.1.1"), ns.network.Ipv4Mask("255.255.255.255"))
ue_ipv4_gateway.Assign(ue_net_device)

# Additional LTE module configuration for base station (eNodeB)
enb_phy = ns.lte.EnbPhy()
enb_phy.SetAttribute("TxPower", ns.core.DoubleValue(30))  # Transmission power in dBm
enb_phy.SetAttribute("AntennaGain", ns.core.DoubleValue(5))  # Antenna gain in dB
enb_phy.SetAttribute("CenterFrequency", ns.core.UintegerValue(2000000000))  # Frequency in Hz

# Additional LTE module configuration for User Equipment (UE)
ue_phy = ns.lte.UePhy()
ue_phy.SetAttribute("TxPower", ns.core.DoubleValue(23))  # Transmission power in dBm
ue_phy.SetAttribute("AntennaGain", ns.core.DoubleValue(2))  # Antenna gain in dB
ue_phy.SetAttribute("CenterFrequency", ns.core.UintegerValue(2000000000))  # Frequency in Hz

# Add the eNodeB and UE to the LTE Helper
lte_helper.AddEnbPhy(enb_phy)
lte_helper.AddUePhy(ue_phy)

# Set up other LTE configurations
# ...

# Configure Evolved Packet Core (EPC) components
epc_helper = ns.lte.LteHelper.DefaultEpcHelper()
epc = epc_helper.GetEpc()

# Connect the LTE helper with the EPC
lte_helper.AttachToEpc(epc)

# Set up the Internet stack on base station
internet_stack_enb = ns.internet.InternetStackHelper()
internet_stack_enb.Install(enb_node)

# Assign IP addresses to devices (base station)
enb_ipv4 = ns.internet.Ipv4AddressHelper()
enb_ipv4.SetBase(ns.network.Ipv4Address("10.1.1.2"), ns.network.Ipv4Mask("255.255.255.0"))
enb_ipv4.Assign(enb_net_device)

# Enable global routing on base station
ns.internet.Ipv4GlobalRoutingHelper.PopulateRoutingTables()

# Set up the simulation time
sim_time = ns.core.Seconds(5)

# Traffic Routing: Implement routing algorithms to direct UE traffic through the LTE network to the internet
ue_default_route = ns.internet.Ipv4StaticRouting()
ue_default_route.SetDefaultRoute(ns.network.Ipv4Address("10.1.1.1"), 1)
ue_node.GetDevice(0).SetAttribute("RoutingProtocol", ns.core.ObjectValue(ue_default_route))

# Run the simulation
ns.core.Simulator.Stop(sim_time)
ns.core.Simulator.Run()
ns.core.Simulator.Destroy()

print("Simulation finished.")

