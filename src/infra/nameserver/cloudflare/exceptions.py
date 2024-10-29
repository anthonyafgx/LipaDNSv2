class MultipleDNSRecordsFoundError(Exception):
    """
    Exception raised when Cloudflare returns more than one record matching the query criteria.

    This commonly happens when there is more than one DNS record with the same content. 
    
    **For example:**: \n
    If you use a method to get a DNS Record by IP from Cloudflare, and you have two DNS records 
    with the same IP, this exception is raised.

    Attributes:
        message (str): Exception message.
        input_dto (CloudflareListDNSRecordsInputDTO): Input DTO (received from Cloudflare) that caused the exception.
    """
    input_dto: 'CloudflareListDNSRecordsInputDTO'

    def __init__(self, input_dto: 'CloudflareListDNSRecordsInputDTO'):
        super().__init__()
        self.input_dto = input_dto

    def __str__(self):
        return f"Cloudflare returned more than one result matching the DNS Record query's criteria. Number of results: {self.input_dto.result_info.count}" # type: ignore
    