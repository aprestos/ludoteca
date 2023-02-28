export default {
  methods: {
    getValidTickets(tickets) {
      const referenceDate = new Date()
      return tickets.filter(
        (ticket) =>
          referenceDate < new Date(ticket.validUntil) &&
          referenceDate > new Date(ticket.validFrom),
      )
    },
  },
}
