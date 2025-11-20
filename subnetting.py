def ip_to_int(a, b, c, d):
    return (a<<24) + (b<<16) + (c<<8) + d

def int_to_ip(n):
    a = (n >> 24) & 0xFF
    b = (n >> 16) & 0xFF
    c = (n >> 8) & 0xFF
    d = n & 0xFF
    return f"{a}.{b}.{c}.{d}"

def hosts_to_prefix(hosts):
    n = 1
    while (2**n - 2) < hosts:
        n += 1
    return 32 - n

def prefix_to_mask(prefix):
    mask = (1 << 32) - (1 << (32 - prefix))
    a = (mask >> 24) & 0xFF
    b = (mask >> 16) & 0xFF
    c = (mask >> 8) & 0xFF
    d = mask & 0xFF
    return mask, f"{a}.{b}.{c}.{d}", f"{a:08b}.{b:08b}.{c:08b}.{d:08b}"

ip_input = input("Introduce la IP de la red principal: ")
prefix_main = int(input("Introduce el prefijo de la red principal (/): "))
octs = [int(x) for x in ip_input.split(".")]
network_int = ip_to_int(octs[0], octs[1], octs[2], octs[3]) & ((1 << 32) - (1 << (32 - prefix_main)))

num_subnets = int(input("Número de subredes: "))
current_network_int = network_int

for i in range(num_subnets):
    hosts = int(input(f"Número de hosts para subred {i+1}: "))
    prefix_sub = hosts_to_prefix(hosts)
    mask_int, mask_dec, mask_bin = prefix_to_mask(prefix_sub)

    network_str = int_to_ip(current_network_int)
    broadcast_int = current_network_int | (~mask_int & 0xFFFFFFFF)
    broadcast_str = int_to_ip(broadcast_int)
    first_host = int_to_ip(current_network_int + 1)
    last_host = int_to_ip(broadcast_int - 1)
    
    total_hosts = broadcast_int - current_network_int - 1

    print(f"\nSubred {i+1}: {network_str}/{prefix_sub}")
    print(f"  Máscara decimal: {mask_dec}")
    print(f"  Máscara binaria: {mask_bin}")
    print(f"  Primer host: {first_host}")
    print(f"  Último host: {last_host}")
    print(f"  Broadcast: {broadcast_str}")
    print(f"  Hosts utilizables: {total_hosts}")

    current_network_int += (2**(32 - prefix_sub))
