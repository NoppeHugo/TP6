import argparse
import subprocess
import sys

#Autheur : Noppe Hugo

def traceroute(target, progressive=False, output_file=None):
    # Commande de base pour traceroute
    command = ["traceroute", target]
    
    # Ouvrir le fichier de sortie si nécessaire
    output = open(output_file, "w") if output_file else None

    try:
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True
        )

        if progressive:
            for line in process.stdout:
                ip = parse_ip_from_line(line)
                if ip:
                    print(ip)
                    if output:
                        output.write(ip + "\n")
        else:
            stdout, stderr = process.communicate()
            if stderr:
                print(f"Erreur : {stderr}", file=sys.stderr)
                return
            ips = [parse_ip_from_line(line) for line in stdout.splitlines()]
            ips = [ip for ip in ips if ip]  # Filtrer les None
            for ip in ips:
                print(ip)
                if output:
                    output.write(ip + "\n")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}", file=sys.stderr)
    finally:
        if output:
            output.close()

def parse_ip_from_line(line):
    # Extraire les adresses IP depuis les lignes de sortie de traceroute
    import re
    match = re.search(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", line)
    return match.group(1) if match else None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Traceroute script with options.")
    parser.add_argument("target", help="URL or IP address to traceroute.")
    parser.add_argument(
        "-p", "--progressive", action="store_true", help="Display results progressively."
    )
    parser.add_argument(
        "-o", "--output-file", help="File to save traceroute results."
    )
    
    args = parser.parse_args()
    traceroute(args.target, progressive=args.progressive, output_file=args.output_file)
