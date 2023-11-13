import dns.resolver
import dns.dnssec

def check_dnssec(domain):
    # Resolve the domain to get its nameservers
    resolver = dns.resolver.Resolver()


    # Check for DS records in the parent domain
    parent_domain = domain.split('.')[-2]
    ds_records = resolver.query(parent_domain, dns.rdtypes.DS).to_text()

    # Check for DNSKEY records in the child domain
    dnskey_records = resolver.query(domain, dns.rdtypes.DNSKEY).to_text()

    # If there are both DS and DNSKEY records, the domain is DNSSEC-enabled
    if ds_records and dnskey_records:
        print(f"{domain} is DNSSEC-enabled")
    else:
        print(f"{domain} is not DNSSEC-enabled")

if __name__ == "__main__":
    domain = input("Enter a domain: ")
    check_dnssec(domain)
